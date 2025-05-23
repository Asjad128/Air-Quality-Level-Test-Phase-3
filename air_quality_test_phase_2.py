# -*- coding: utf-8 -*-
"""Air_Quality_Test_Phase_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UaEei7WI_fsOLsz_Wv2hY4WGHHz8B3DO
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('city_day.csv')

df.head()



# Drop rows with missing AQI or AQI_Bucket
df = df.dropna(subset=['AQI', 'AQI_Bucket'])

# Select relevant features (pollutants)
pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']

# Fill missing pollutant values with median
for col in pollutants:
    df[col].fillna(df[col].median(), inplace=True)

# Encode target variable
label_encoder = LabelEncoder()
df['AQI_Bucket_Encoded'] = label_encoder.fit_transform(df['AQI_Bucket'])

# Feature scaling
scaler = StandardScaler()
X = scaler.fit_transform(df[pollutants])
y = df['AQI_Bucket_Encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Print classification report
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Plot confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

importances = model.feature_importances_
feature_names = df[pollutants].columns
sns.barplot(x=importances, y=feature_names)
plt.title('Feature Importance for AQI Bucket Prediction')
plt.xlabel('Importance')
plt.ylabel('Pollutant')
plt.show()