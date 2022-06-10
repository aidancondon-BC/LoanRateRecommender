# This file was used to test my model and find the optimal parameters for XGBClassifier()
# The link to the dataset is https://www.kaggle.com/datasets/itssuru/loan-data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import accuracy_score

df = pd.read_csv('loan_data.csv', engine='python')

features = ["creditPolicy","purpose","intRate","installment","logAnnualinc","dti","fico",
        "daysWithCrLine","revolBal","revolUtil","inqLast6mths","delinq2yrs","pubRec"]

X = df[features]
y = df.notfullypaid

s = (X.dtypes == 'object')
object_cols = list(s[s].index)
label_X = X.copy()
og_encoder = OrdinalEncoder()
label_X[object_cols] = og_encoder.fit_transform(X[object_cols])

X = label_X

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1) 

y_vals = []
for x in range(5, 50):
    fitted_model = XGBClassifier(n_estimators=x, learning_rate=0.5)
    fitted_model.fit(train_X, train_y)
    final_pred = fitted_model.predict(val_X)
    acc = accuracy_score(val_y, final_pred)
    y_vals.append(acc)
    print(f'{x} ––> Accuracy Score: {acc}')

plt.plot(range(5, 50), y_vals)
plt.show()