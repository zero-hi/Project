import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

import pickle

df = pd.read_csv("C:/Users/wdit0/Desktop/Section3 Project/project_app/cadio_1.csv" , encoding='euc-kr')

features = df.drop(columns =['cardio'], axis = 1)
target = df['cardio']

X_train = features
y_train = target

model = make_pipeline( 
        SimpleImputer(), 
        RandomForestClassifier(n_estimators=100 ,random_state=2, n_jobs=-1)
)

model.fit(X_train, y_train)

with open('model.pkl','wb') as pickle_file:
    pickle.dump(model, pickle_file)