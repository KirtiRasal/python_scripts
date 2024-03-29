import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("C:/Users/sneha/OneDrive/Desktop/Snehal/Masters_Study/Study-SEM2/CaseStudy_Pwc/SAMPLE.csv")

print(df)
# print(df.dtypes)

# Convert class variables type to object
df['isFraud'] = df['isFraud'].astype('object')
df['Type_code'] = df['Type_code'].astype('object')
print(df.dtypes)

# summary statistics of numerical and categorical variables
print(df.describe(include='all'))

print('Maximum number of missing values in any column: ' + str(df.isnull().sum().max()))

# Check the percent value of isfraud column(0/1)

# Plot bar graph displaying the count of transactions based on Type of Transaction

# Check fraud transactions by transaction type

# Retaining only CASH-OUT and TRANSFER transactions
# df = df.loc[df['type'].isin(['CASH_OUT', 'TRANSFER']),:]
# print('The new data now has ', len(df), ' transactions.')

# Check that there are no negative amounts
print('Number of transactions where the transaction amount is negative: ' + str(sum(df['amount'] < 0)))

# Check instances where transacted amount is 0
print('Number of transactions where the transaction amount is equal to zero: ' + str(sum(df['amount'] == 0)))

# Remove 0 amount values if there are any present
#df = df.loc[df['amount'] > 0,:]

# The recipient's final balance should be equal to the recipient's initial balance plus the transaction amount.
# Similarly, the originator's final balance should be equal to originator's initial balance minus the transaction amount.

print('Number of transactions where the originator initial balance is equal to zero: ' + str(sum(df['oldbalanceOrg'] == 0)))

print('Number of transactions where the recipient final balance is equal to zero: ' + str(sum(df['newbalanceDest'] == 0)))

#check fraud and non-fraud transactions count by time step.

#Check differences between fraud and non-fraud transactions in terms of transaction amount.

# Defining inaccuracies in originator and recipient balances
df['origBalance_inacc'] = (df['oldbalanceOrg'] - df['amount']) - df['newbalanceOrg']
df['destBalance_inacc'] = (df['oldbalanceDest'] + df['amount']) - df['newbalanceDest']

print(df)

#Plot distribution of inaccuracy in originator account balances.

#Plot distribution of inaccuracy in destination account balances.

# Removing name columns
df = df.drop(['nameOrig', 'nameDest'], axis=1)

# Creating dummy variables through one hot encoding for 'type' column
df = pd.get_dummies(df, columns=['Type'], prefix=['Type'])

# Normalization of the dataset
std_scaler = StandardScaler()
df_scaled = pd.DataFrame(std_scaler.fit_transform(df.loc[:,~df.columns.isin(['isFraud'])]))
df_scaled.columns = df.columns[:-1]
df_scaled['isFraud'] = df['isFraud']

X = df_scaled.loc[:, df_scaled.columns != 'isFraud']
y = df_scaled.loc[:, df_scaled.columns == 'isFraud']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 0)
label_encoder = preprocessing.LabelEncoder()
y_train = label_encoder.fit_transform(y_train.values.ravel())
y_test = label_encoder.fit_transform(y_test.values.ravel())


from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=20, random_state=0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))