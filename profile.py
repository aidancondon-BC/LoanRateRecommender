import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 'loan_data.csv' found in https://www.kaggle.com/datasets/itssuru/loan-data
df = pd.read_csv('loan_data.csv', engine='python')

class Profile:
    
    credit_policy = None
    purpose = None
    int_rate = None
    installment = None
    log_annual_inc = None
    dti = None
    fico = None
    days_with_cr_line = None
    revol_bal = None
    revol_util = None
    inq_last_SixMths = None
    delinq_TwoYrs = None
    pub_rec = None
    not_fully_paid = None

    # only data that we don't have in 'loan_data.csv'
    len_of_loan = None

    def __init__(self):
        self.credit_policy = int(input("Enter Credit Policy (1 or 0): "))
        print("\n\tEnter 0 for Debt Consolidation")
        print("\tEnter 1 for Credit Card")
        print("\tEnter 2 for All Other")
        print("\tEnter 3 for Home Improvement")
        print("\tEnter 4 for Small Business")
        print("\tEnter 5 for Major Purchase")
        print("\tEnter 6 for Educational\n")
        self.purpose = (df[df.columns[1]]).unique()[int(input("Select Purpose: "))]
        self.installment = float(input("Enter Installment: "))
        self.log_annual_inc = float(input("Enter the natural log of the annual income given by applicant: "))
        self.dti = float(input("Enter the debt-to-income ratio of the applicant: "))
        self.fico = int(input("Enter the user's FICO score: "))
        self.days_with_cr_line = float(input("Enter the number of days the user has had a credit line: "))
        self.revol_bal = int(input("Enter the Revolving Balance: "))
        self.revol_util = float(input("Enter the Revolving Line Utilization Rate: "))
        self.inq_last_SixMths = int(input("Enter the Applicant's number of inquiries from creditors over the past 6 months: "))
        self.delinq_TwoYrs = int(input("Enter the number of times the applicant has been 30+ days past due on a payment in the previous 2 years: "))
        self.pub_rec = int(input("Enter the applicants number of derogatory public records: "))
        self.len_of_loan = int(input("Enter the total period of the loan in months:"))

    """
    If you don't want to go through the process of entering data in the terminal
    you can just use this constructor below instead, and put True as a parameter for the 
    constructor
    """
    def __init__(self, isTest):
        self.credit_policy = 1 
        self.purpose = 2.0
        self.int_rate = 0.1189
        self.installment = 829.1
        self.log_annual_inc = 11.350407
        self.dti = 19.48
        self.fico = 737
        self.days_with_cr_line = 5639.958333
        self.revol_bal = 28854
        self.revol_util = 52.1
        self.delinq_TwoYrs = 1.0
        self.inq_last_SixMths = 0
        self.pub_rec = 0
        self.len_of_loan = 60

    def get_data(self):
        dct = {"creditPolicy": self.credit_policy,
                "purpose": self.purpose,
                "intRate": self.int_rate,
                "installment": self.installment,
                "logAnnualinc": self.log_annual_inc,
                "dti": self.dti,
                "fico": self.fico,
                "daysWithCrLine": self.days_with_cr_line,
                "revolBal": self.revol_bal,
                "revolUtil": self.revol_util,
                "inqLast6mths": self.inq_last_SixMths,
                "delinq2yrs": self.delinq_TwoYrs,
                "pubRec": self.pub_rec}
        return pd.DataFrame(data=dct, index=[0])
    
    # Changing the interest rate also changes the monthly installment
    def set_int_rate(self, rate):
        self.int_rate = rate
        numerator = rate * ((1 + rate) ** self.len_of_loan)
        denominator = ((1 + rate) ** self.len_of_loan) - 1
        self.installment = self.revol_bal * (numerator / denominator)