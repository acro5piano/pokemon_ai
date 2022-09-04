from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

dataset = load_digits()
image_shape = (8, 8, 1)
num_class = 10


y = dataset.target  # type: ignore
X = dataset.data  # type: ignore

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


estimator = RandomForestClassifier()
estimator.fit(X_train, y_train)

print(classification_report(y_test, estimator.predict(X_test)))
