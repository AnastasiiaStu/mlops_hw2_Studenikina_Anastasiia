import pickle
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42,
    max_depth=5
)
model.fit(X_train, y_train)

train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print(f"на обучающей выборке: {train_accuracy:.4f}")
print(f"на тестовой выборке: {test_accuracy:.4f}")

sample = X_test[0].reshape(1, -1)
prediction = model.predict(sample)[0]
probabilities = model.predict_proba(sample)[0]

print(f"признаки: {sample[0]}")
print(f"педсказанный класс: {prediction} ({iris.target_names[prediction]})")
print(f"увренность: {probabilities[prediction]:.4f}")

model_path = 'models/model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)