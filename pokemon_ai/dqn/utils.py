from random import sample

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p


def build_random_team() -> list[p.Pokemon]:
    pokemons = [
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
    ]
    return sample(pokemons, 6)
