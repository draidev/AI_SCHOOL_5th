# Data Manipulation 
from re import X
import numpy as np
import pandas as pd

# Visualization 
import matplotlib.pyplot as plt
import missingno
import seaborn as sns
from pandas.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D

# Feature Selection and Encoding
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, label_binarize, StandardScaler
# https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Machine learning 
import sklearn.ensemble as ske
from sklearn import datasets, model_selection, tree, preprocessing, metrics, linear_model,neighbors
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor, ExtraTreesClassifier
from sklearn.metrics import *
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier 
from vecstack import stacking

#사용자 함수----------------------------------------------------------------------
def pipe_processing(train_df, test_df):
    num_features = []
    cat_features = []

    # 데이터타입에 따라 numeric과 categorical을 나눈다
    for col in train_df.columns:
        if train_df[col].dtypes == object:
            cat_features.append(col)
        else:
            num_features.append(col)

    #Pipeline
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(categories='auto', handle_unknown = 'ignore')

    preprocessor = ColumnTransformer(
        transformers=[ # List of (name, transformer, column(s))
            ('num', numeric_transformer, num_features),
            ('cat',categorical_transformer,cat_features)
        ]
    )

    preprocessor_pipe = Pipeline(steps=[('preprocessor', preprocessor)])
    preprocessor_pipe.fit(train_df)

    train_df_transformed = preprocessor_pipe.transform(train_df)
    test_df_transformed = preprocessor_pipe.transform(test_df)

    return train_df_transformed, test_df_transformed

def fillna_with_ML(df, col_name):
    not_na_rows = df[df[col_name].notnull()]
    train_x = not_na_rows.drop([col_name],axis=1)
    train_y = not_na_rows[col_name]

    na_rows = df[df[col_name].isnull()]
    test_x = na_rows.drop([col_name],axis=1)

    train_x_transformed, test_x_transformed = pipe_processing(train_x, test_x)

    model = GradientBoostingRegressor(n_estimators=200, random_state=0)
    model.fit(train_x_transformed, train_y)
    test_y = model.predict(test_x_transformed)

    na_rows[col_name] = test_y

    df = pd.concat([not_na_rows, na_rows],axis=0).sort_index()

    return df

#-----------------------------------------------------------------------------


tit_df = pd.read_csv('titanic.csv')
print(tit_df.head())

x_data = tit_df.copy()
del x_data['Survived']
y_data = tit_df[['Survived']]


x_data['FamilyNum'] = x_data['SibSp'] + x_data['Parch']
x_data = x_data.drop(['PassengerId','Cabin'],axis=1)

name_title = pd.DataFrame(i.split(',')[1].split(' ')[1] for i in x_data['Name'])

for title in name_title.iterrows:
    if title[1][0] not in ['Mr.','Mrs.','Miss.','Master.','Dr.']:
        name_title.iloc[title[0]] = 'Others'

x_data['NameTitle'] = name_title