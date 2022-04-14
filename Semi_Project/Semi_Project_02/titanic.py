import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from collections import Counter
import math
import seaborn as sns

from sklearn import datasets, model_selection, linear_model
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

tit_df = pd.read_csv('titanic.csv')
print(tit_df.head())
