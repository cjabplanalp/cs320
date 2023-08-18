import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class UserPredictor():
    def __init__(self):
        self.model = LogisticRegression()
    
    def fit(self, user_file, log_file, y_file):
        #edit df to have useful columns
        df1 = user_file.merge(y_file)
        edit = log_file.groupby('user_id', as_index = False).sum()
        df1 = df1.merge(edit, on = 'user_id', how = 'left')
        df1['seconds'] = df1['seconds'].fillna(0)
        
        #fit the model
        self.model.fit(df1[['past_purchase_amt', 'seconds']], df1[['y']])
        
    def predict(self, test_user_file, test_log_file):
        other_edit = test_log_file.groupby('user_id', as_index = False).sum()
        df2 = test_user_file.merge(other_edit, on = 'user_id', how = 'left')
        df2['seconds'] = df2['seconds'].fillna(0)
        
        return self.model.predict(df2[['past_purchase_amt','seconds']])
    