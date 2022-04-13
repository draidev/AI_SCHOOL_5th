from sklearn import datasets, model_selection, metrics, svm
import joblib

""" Scikit-learn modeling(5-steps) """
iris = datasets.load_iris()
train_x, test_x, train_y, test_y = model_selection.train_test_split(iris.data, iris.target, test_size=0.3, random_state=0)

model = svm.SVC(C=1.0, gamma='auto')
model.fit(train_x, train_y)

predicted_y = model.predict(test_x)
print(metrics.accuracy_score(predicted_y, test_y))

""" Saving the trained model """
joblib.dump(model, 'model_iris_svm_v1.pkl', compress=True)

""" Loading the trained model """
model_loaded = joblib.load('model_iris_svm_v1.pkl')

print(metrics.accuracy_score(model_loaded.predict(test_x), test_y))