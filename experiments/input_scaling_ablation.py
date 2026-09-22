"""Compare raw, scaled, and one-hot observations in the archived DQN.

The default ``raw`` and ``scaled`` modes reproduce the input-scaling ablation.
Two optional modes isolate categorical encoding:

* ``species_onehot``: one-hot species, HP fraction, scaled move IDs;
* ``onehot``: one-hot species and every move slot, plus HP fraction.

The network's hidden layers, opponent curriculum, rewards, replay buffer, update
frequency, and unmasked TD target are left unchanged.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import platform
import random
import statistics
import time
import warnings
from collections.abc import Callable
from pathlib import Path

import numpy as np
import sklearn
from sklearn.neural_network import MLPRegressor

from pokemon_ai.dqn.trainer import Trainer
from pokemon_ai.dqn.utils import build_random_team
from pokemon_ai.dqn.value_function_agent import NeuralNetworkPlayer, ValueFunctionAgent
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.pokedex import Pokemon, calculate_actual_hp
from pokemon_ai.simulator.player import Player
from pokemon_ai.simulator.sample_players import JustAttackPlayer, StupidRandomPlayer

MAX_SPECIES_ID = 135
MAX_MOVE_ID = 9
SPECIES_IDS = (112, 121, 135)
MOVE_IDS = tuple(range(1, 10))
OBSERVATION_SIZES = {
    "raw": 84,
    "scaled": 84,
    "species_onehot": 108,
    "onehot": 492,
}
RAW_TO_ARRAY = Pokemon.to_array


def scaled_to_array(self: Pokemon) -> list[float]:
    """Return the original six features with every value bounded to 0..1."""
    return [
        self.id / MAX_SPECIES_ID,
        max(0, self.actual_hp) / calculate_actual_hp(self.hp),
        *[move.id / MAX_MOVE_ID for move in self.actual_moves],
    ]


def one_hot(value: int, categories: tuple[int, ...]) -> list[float]:
    """Encode a category without inventing an order or distance."""
    return [1.0 if value == category else 0.0 for category in categories]


def species_onehot_to_array(self: Pokemon) -> list[float]:
    """One-hot the species while leaving move IDs scaled scalars."""
    return [
        *one_hot(self.id, SPECIES_IDS),
        max(0, self.actual_hp) / calculate_actual_hp(self.hp),
        *[move.id / MAX_MOVE_ID for move in self.actual_moves],
    ]


def onehot_to_array(self: Pokemon) -> list[float]:
    """One-hot both species and each move slot."""
    result = [
        *one_hot(self.id, SPECIES_IDS),
        max(0, self.actual_hp) / calculate_actual_hp(self.hp),
    ]
    for move in self.actual_moves:
        result.extend(one_hot(move.id, MOVE_IDS))
    return result


def set_observation_mode(mode: str) -> None:
    encoders: dict[str, Callable[[Pokemon], list[float]]] = {
        "raw": RAW_TO_ARRAY,
        "scaled": scaled_to_array,
        "species_onehot": species_onehot_to_array,
        "onehot": onehot_to_array,
    }
    Pokemon.to_array = encoders[mode]  # type: ignore[method-assign]


def reset_rng(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def new_model(mode: str, seed: int) -> MLPRegressor:
    """Construct the archived 10x10 MLP for the selected input width."""
    reset_rng(seed)
    model = MLPRegressor(hidden_layer_sizes=(10, 10), max_iter=200)
    fake_state = np.array([np.zeros(OBSERVATION_SIZES[mode])])
    fake_estimation = np.array([np.zeros(10)])
    # The archived path initializes once in new_model and once when Trainer
    # wraps that model. Repeat both zero-target updates for a fair comparison.
    model.partial_fit(fake_state, fake_estimation)
    model.partial_fit(fake_state, fake_estimation)
    return model


def train(mode: str, seed: int, episodes: int):
    set_observation_mode(mode)
    reset_rng(seed)
    Trainer.experiences.clear()

    # ValueFunctionAgent hard-codes 84 inputs in __init__. Build the archived
    # objects without that constructor so one-hot observations can be wider;
    # reset() and update() remain the unmodified production methods.
    agent = ValueFunctionAgent.__new__(ValueFunctionAgent)
    agent.model = new_model(mode, seed)
    agent.epsilon = 0.2
    trainer = Trainer.__new__(Trainer)
    trainer.agent = agent
    trainer.episodes = episodes
    trainer.step = 0
    # The archived trainer prints progress every 100 episodes. Keep ablation
    # output machine-readable by suppressing those progress messages.
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        trainer.train()
    return trainer.agent.model


def evaluate(
    model, mode: str, opponent_type: type[Player], seed: int, battles: int
) -> dict:
    set_observation_mode(mode)
    reset_rng(seed)
    wins = losses = draws = 0

    for _ in range(battles):
        learner = NeuralNetworkPlayer(build_random_team(), model, epsilon=0.0)
        opponent = opponent_type(build_random_team())
        battle = Battle(learner, opponent)
        battle.validate()

        while battle.get_winner() is None and battle.turn <= 500:
            battle.forward_step()

        winner = battle.get_winner()
        if winner is learner:
            wins += 1
        elif winner is opponent:
            losses += 1
        else:
            draws += 1

    return {
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": wins / battles,
    }


def diagnostic_states(mode: str) -> np.ndarray:
    """Build the same ten physical battle states for each input encoder."""
    set_observation_mode(mode)
    previous_state = random.getstate()
    random.seed(20260922)
    states: list[list[float]] = []

    try:
        for state_index in range(10):
            player1 = Player(build_random_team())
            player2 = Player(build_random_team())
            player1.active_pokemon_index = state_index % 6
            player2.active_pokemon_index = (state_index * 3 + 1) % 6

            for side_index, player in enumerate((player1, player2)):
                for slot, pokemon in enumerate(player.pokemons):
                    max_hp = calculate_actual_hp(pokemon.hp)
                    damage_fraction = ((state_index + slot + side_index * 2) % 8) / 8
                    pokemon.actual_hp = max(0, round(max_hp * (1 - damage_fraction)))

            states.append(Battle(player1, player2).to_array())
    finally:
        random.setstate(previous_state)

    return np.asarray(states, dtype=float)


def diagnose(model, mode: str) -> dict:
    states = diagnostic_states(mode)
    first_layer = states @ model.coefs_[0] + model.intercepts_[0]
    activations = np.maximum(0.0, first_layer)
    q_values = model.predict(states)
    q_ranges = np.ptp(q_values, axis=0)

    return {
        "input_min": float(states.min()),
        "input_max": float(states.max()),
        "active_first_layer_units": int(np.any(activations > 1e-12, axis=0).sum()),
        "total_first_layer_units": int(activations.shape[1]),
        "varying_q_outputs": int((q_ranges > 1e-9).sum()),
        "max_q_range_across_states": float(q_ranges.max()),
    }


def summarize(runs: list[dict], modes: list[str]) -> dict:
    summary: dict[str, dict] = {}
    for mode in modes:
        selected = [run for run in runs if run["mode"] == mode]
        mode_summary: dict[str, object] = {}
        for opponent in ("random", "attack"):
            rates = [run["evaluation"][opponent]["win_rate"] for run in selected]
            mode_summary[f"{opponent}_win_rate_mean"] = statistics.mean(rates)
            mode_summary[f"{opponent}_win_rate_stdev"] = (
                statistics.stdev(rates) if len(rates) > 1 else 0.0
            )
        active = [run["diagnostics"]["active_first_layer_units"] for run in selected]
        varying = [run["diagnostics"]["varying_q_outputs"] for run in selected]
        mode_summary["active_first_layer_units_mean"] = statistics.mean(active)
        mode_summary["varying_q_outputs_mean"] = statistics.mean(varying)
        summary[mode] = mode_summary
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=1000)
    parser.add_argument("--battles", type=int, default=300)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=tuple(OBSERVATION_SIZES),
        default=["raw", "scaled"],
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.monotonic()
    runs: list[dict] = []

    for seed in args.seeds:
        for mode in args.modes:
            run_started = time.monotonic()
            model = train(mode, seed, args.episodes)
            result = {
                "seed": seed,
                "mode": mode,
                "evaluation": {
                    "random": evaluate(
                        model, mode, StupidRandomPlayer, 100_000 + seed, args.battles
                    ),
                    "attack": evaluate(
                        model, mode, JustAttackPlayer, 200_000 + seed, args.battles
                    ),
                },
                "diagnostics": diagnose(model, mode),
                "elapsed_seconds": time.monotonic() - run_started,
            }
            runs.append(result)
            print(json.dumps(result, ensure_ascii=False))

    experiment_name = (
        "input-scaling-ablation"
        if args.modes == ["raw", "scaled"]
        else "categorical-encoding-ablation"
    )
    output = {
        "experiment": experiment_name,
        "encodings": {
            "raw": "scalar species ID, raw HP, scalar move IDs",
            "scaled": "scaled species ID, HP fraction, scaled move IDs",
            "species_onehot": "one-hot species, HP fraction, scaled move IDs",
            "onehot": "one-hot species, HP fraction, one-hot move per slot",
        },
        "observation_sizes": OBSERVATION_SIZES,
        "unchanged": [
            "10x10 hidden layers",
            "opponent curriculum",
            "reward",
            "replay buffer",
            "one update per battle",
            "unmasked TD target",
        ],
        "modes": args.modes,
        "episodes": args.episodes,
        "evaluation_battles_per_opponent": args.battles,
        "seeds": args.seeds,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "runs": runs,
        "summary": summarize(runs, args.modes),
        "elapsed_seconds": time.monotonic() - started,
    }

    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
