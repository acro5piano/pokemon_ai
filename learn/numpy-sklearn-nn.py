import numpy as np
from sklearn.neural_network import MLPRegressor

image_shape = (8, 8, 1)
num_class = 10


X = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
    ]
)

y = np.array(
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
)


estimator = MLPRegressor()
estimator.fit(X, y)

print(estimator.predict(X))
X_test = np.array(
    [
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
    ]
)
print(estimator.predict(X_test))
