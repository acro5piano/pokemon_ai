from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pokemon_ai.simulator.battle import Battle


class ValueFunctionAgent:
    def __init__(self):
        self.model = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=(10, 10),
                        max_iter=1,
                    ),
                ),
            ]
        )
