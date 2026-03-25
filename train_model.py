import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ================= CREATE MODEL FOLDER =================
os.makedirs("model", exist_ok=True)

# ================= LOAD DATA =================
df = pd.read_csv(r"C:\Traffic_signal\data\final_merged_traffic_dataset.csv")

print("Columns:", df.columns)

# ================= HANDLE DATETIME =================
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = pd.to_datetime(df[col])
            df["hour"] = df[col].dt.hour
            df.drop(col, axis=1, inplace=True)
        except:
            pass

# ================= TARGET =================
y = df.iloc[:, -1]

if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y)
    pickle.dump(le, open("model/label_encoder.pkl", "wb"))

# ================= FEATURES =================
X = df.iloc[:, :-1]
X = X.select_dtypes(include=['number'])

# ================= TRAIN =================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# ================= SAVE =================
pickle.dump(model, open("model/model.pkl", "wb"))

print("✅ Model trained successfully")