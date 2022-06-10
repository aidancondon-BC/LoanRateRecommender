import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from profile import Profile as prof
from xgboost import XGBClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_absolute_error

class Recommendation:
    
    # 'loan_data.csv' found in https://www.kaggle.com/datasets/itssuru/loan-data
    df = pd.read_csv('loan_data.csv', engine='python')
    applicant = prof(True)
    
    # Accuracy Score of roughly 83% based on calculations made in optimize.py file
    def make_model(self):
        features = ["creditPolicy","purpose","intRate","installment","logAnnualinc","dti","fico",
                "daysWithCrLine","revolBal","revolUtil","inqLast6mths","delinq2yrs","pubRec"]
        X = self.df[features]
        y = self.df.notfullypaid

        s = (X.dtypes == 'object')
        object_cols = list(s[s].index)
        label_X = X.copy()
        label_X[object_cols] = OrdinalEncoder().fit_transform(X[object_cols])

        fitted_model = XGBClassifier(n_estimators=30, learning_rate=0.5)
        fitted_model.fit(label_X, y)

        return fitted_model

    def predict_based_on_rates(self, rates):
        model = self.make_model()
        predictions = []
        for rate in rates:
            self.applicant.set_int_rate(rate)
            cur_pred = model.predict(self.applicant.get_data())[0]
            predictions.append((rate,cur_pred))
        return predictions

    def get_rec(self):
        data = self.predict_based_on_rates(np.linspace(0.01, 1, num=500))
        rec = data[([x[1] for x in data].index(1) - 1)]
        return rec[0]

rec = Recommendation().get_rec()
print(f'Model Recommends Interest Rate of {rec}')

