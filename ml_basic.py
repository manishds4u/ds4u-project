# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 18:25:07 2019

@author: Manish
"""

import pandas as pd
import numpy as np


data=pd.read_csv("crop_production.csv")

df=pd.DataFrame(data)

df.dropna(inplace=True)

from sklearn.preprocessing import LabelEncoder
seasonl = LabelEncoder()
districtl = LabelEncoder()
statel = LabelEncoder()
crop1=LabelEncoder()

df['season_enc'] = seasonl.fit_transform(df['Season'].str.lower())
df['district_enc'] = districtl.fit_transform(df['District_Name'].str.lower())
df['state_enc'] =statel.fit_transform(df['State_Name'].str.lower())
df['crop_en'] = crop1.fit_transform(df['Crop'].str.lower())

crop_zip = dict(zip(crop1.classes_, crop1.transform(crop1.classes_)))
crop_df = pd.DataFrame(list(crop_zip.items()), columns=['crop', 'cropValue'])

season_zip = dict(zip(seasonl.classes_, seasonl.transform(seasonl.classes_)))
season_df = pd.DataFrame(list(season_zip.items()), columns=['season', 'seasonValue'])

district_zip = dict(zip(districtl.classes_, districtl.transform(districtl.classes_)))
district_df = pd.DataFrame(list(district_zip.items()), columns=['district', 'districtValue'])

state_zip = dict(zip(statel.classes_, statel.transform(statel.classes_)))
state_df = pd.DataFrame(list(state_zip.items()), columns=['state', 'stateValue'])



features=df.iloc[:,[9,8,2,7,5,6]].values
col=["state","district","crop_year","season","area","production"]
features=pd.DataFrame(features, columns=col )

labels=df.iloc[:,10].values
labels=pd.DataFrame(labels, columns=["crop"])

from sklearn.model_selection import  train_test_split
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.1, random_state=42)


from sklearn.ensemble import RandomForestClassifier
rfc=RandomForestClassifier( max_features='log2',verbose=1,n_jobs=2 ,n_estimators= 20, max_depth=None, criterion='gini')

rfc.fit(x_train,y_train)

prediction=rfc.predict(x_test)


from sklearn.metrics import accuracy_score
score=accuracy_score(y_test, prediction)



prediction=pd.DataFrame(prediction, columns=["cpred"])


cinv = list(crop1.inverse_transform(prediction['cpred']))
cinv_df = pd.DataFrame(np.array([cinv]).T, columns=["crop_inv"])


prd_con=pd.concat([prediction, cinv_df], ignore_index=True, sort =False, axis=1)

