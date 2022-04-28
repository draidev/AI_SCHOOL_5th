from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from vecstack import stacking
from vecstack import StackingTransformer

""" 1. Functional API """
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=0)

models = [
    ExtraTreesClassifier(random_state=0, n_jobs=-1, n_estimators=100, max_depth=3),
    RandomForestClassifier(random_state=0, n_jobs=-1,n_estimators=100, max_depth=3),
    XGBClassifier(seed=0,n_jobs=-1, learning_rate=0.1, n_estimator=100,max_depth=3)
    ]

S_train, S_test = stacking(
    models,
    X_train, y_train, X_test,
    regression=False,
    metric=accuracy_score,
    n_folds=4, stratified=True, shuffle=True,
    random_state=0, verbose=2
)

model = XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimator=100, max_depth=3, eval_metric='mlogloss')
model = model.fit(S_train,y_train)
y_pred = model.predict(S_test)

print('최종 prediction score : [{:.4f}%]'.format(accuracy_score(y_pred,y_test)*100))

print("2. Scikit-learn API-----------------------------------------------------")
print("------------------------------------------------------------------------")

""" 2. Scikit-learn API """
iris = load_iris() 
X, y = iris.data, iris.target 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# 1st level estimator 초기화
estimators = [ 
    ('ExtraTrees', ExtraTreesClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3)),
    ('RandomForest', RandomForestClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3)),
    ('XGB', XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimators = 100, max_depth = 3, eval_metric='mlogloss'))]

stack = StackingTransformer(estimators, 
                            regression = False, 
                            metric = accuracy_score, 
                            n_folds = 4, stratified = True, shuffle = True, 
                            random_state = 0, verbose = 2)

stack = stack.fit(X_train, y_train)

S_train = stack.transform(X_train)
S_test = stack.transform(X_test)

# 2nd level estimator 
model = XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimators = 100, max_depth = 3, eval_metric='mlogloss') 
model = model.fit(S_train, y_train) 

y_pred = model.predict(S_test) 
print('최종 prediction score : [{:.4f}%]'.format(accuracy_score(y_pred,y_test)*100))