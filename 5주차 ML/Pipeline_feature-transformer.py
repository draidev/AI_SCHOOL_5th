import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import datasets, model_selection, linear_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier


""" 1. 데이터 가져오기, 전처리 """
df_data = pd.read_excel('boston_house_data.xlsx', index_col=0)
df_data.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

df_target = pd.read_excel('boston_house_target.xlsx', index_col=0)
df_target.columns = ['Price']

mean_price = df_target['Price'].mean()
df_target['Price'] = df_target['Price'].apply(lambda x: 1 if x>mean_price else 0)

print(df_data['RAD'].value_counts(sort=False))
print()
print(df_data.head(3))
print()
print(df_target.head(3))
print()

""" 2. train-test split """
x_train, x_test, y_train, y_test = model_selection.train_test_split(
    df_data, df_target, test_size=0.3, random_state=0
)

""" 3. 파이프라인 만들기(StandardScaler & OneHotEncoder """
numeric_features = ['CRIM', 'ZN', 'INDUS', 'NOX', 'RM', 'AGE', 'DIS', 'TAX', 'PTRATIO', 'B', 'LSTAT']
numeric_transformer = StandardScaler()

categorical_features = ['CHAS', 'RAD']
categorical_transformer = OneHotEncoder(categories='auto', handle_unknown='ignore') # 'ignore : 기존에 없는 카테고리 데이터가 있을 떄 무시한다'

preprocessor = ColumnTransformer(
    transformers=[
        ('num',numeric_transformer,numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

""" 4. 파이프라인 사용 """
preprocessor_pipe = Pipeline(steps=[('preprocessor', preprocessor)])
preprocessor_pipe.fit(x_train)

x_train_transformed = preprocessor_pipe.transform(x_train)
x_test_transformed = preprocessor_pipe.transform(x_test)

print(x_train_transformed[0])
print()
print(pd.DataFrame(x_train_transformed).head(3))
print()

model = GradientBoostingClassifier(n_estimators=200, random_state=0)
model.fit(x_train_transformed, y_train)

accuracy = model.score(x_test_transformed, y_test)
print("model score : ", round(accuracy, 4))