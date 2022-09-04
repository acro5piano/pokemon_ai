import numpy as np
import tensorflow as tf
from sklearn.datasets import load_digits
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

dataset = load_digits()
image_shape = (8, 8, 1)
num_class = 10


y = tf.keras.utils.to_categorical(dataset.target, 10)  # type: ignore
X = np.array([data.reshape(image_shape) for data in dataset.data])  # type: ignore


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = tf.keras.Sequential(
    [
        tf.keras.layers.Conv2D(
            5, kernel_size=3, strides=1, padding="same", activation="relu", input_shape=image_shape
        ),
        tf.keras.layers.Conv2D(
            3,
            kernel_size=2,
            strides=1,
            padding="same",
            activation="relu",
        ),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=num_class, activation="softmax"),
    ]
)
model.compile(optimizer="sgd", loss="categorical_crossentropy")
model.fit(X_train, y_train, epochs=500)

y_true = np.argmax(y_test, axis=1)
y_pred = np.argmax(model.predict(X_test), axis=1)

print(classification_report(y_true, y_pred))
