import pandas as pd
import joblib
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

# Učitaj modele
model_rf = joblib.load("./models/model_rf.pkl")
scaler = joblib.load("./models/scaler.pkl")
model_dl = tf.keras.models.load_model("./models/model_dl.keras")

def preprocess_input(data: dict):
    # Mapiranje input ključeva u točne nazive koje modeli očekuju
    mapping = {
        "math_percentage": "math percentage",
        "reading_score_percentage": "reading score percentage",
        "writing_score_percentage": "writing score percentage",
        "race_ethnicity": "race/ethnicity",
        "parental_level_of_education": "parental level of education",
        "test_preparation_course": "test preparation course"
    }

    # Mapiraj podatke
    mapped_data = {mapping.get(k, k): v for k, v in data.items()}
    
    df = pd.DataFrame([mapped_data])

     # 🔁 Dodano mapiranje vrijednosti ako dođu u skraćenom obliku
    df['sex'] = df['sex'].replace({'F': 'female', 'M': 'male'})
    df['race/ethnicity'] = df['race/ethnicity'].replace({
        'A': 'group A', 'B': 'group B', 'C': 'group C', 'D': 'group D', 'E': 'group E'
    })

    # Label encoderi sa poznatim klasama
    le_sex = LabelEncoder().fit(['female', 'male'])
    le_race = LabelEncoder().fit(['group A', 'group B', 'group C', 'group D', 'group E'])
    le_parent_edu = LabelEncoder().fit([
        "some high school", "high school", "some college",
        "associate's degree", "bachelor's degree", "master's degree"
    ])
    le_lunch = LabelEncoder().fit(['free/reduced', 'standard'])
    le_test_prep = LabelEncoder().fit(['none', 'completed'])

    # Kodiraj kategorijske varijable
    df['sex'] = le_sex.transform(df['sex'])
    df['race/ethnicity'] = le_race.transform(df['race/ethnicity'])
    df['parental level of education'] = le_parent_edu.transform(df['parental level of education'])
    df['lunch'] = le_lunch.transform(df['lunch'])
    df['test preparation course'] = le_test_prep.transform(df['test preparation course'])
    
    # TOČNO sortiraj stupce po onome što model_rf očekuje
    required_cols = ['race/ethnicity', 'parental level of education', 'lunch',
                     'test preparation course', 'math percentage', 'reading score percentage',
                     'writing score percentage', 'sex']
    df = df[required_cols]

    return df

def predict_rf(data: dict):
    df = preprocess_input(data)
    pred = model_rf.predict(df)[0]
    return int(pred)

def predict_dl(data: dict):
    df = preprocess_input(data)
    df_scaled = scaler.transform(df)
    pred_prob = model_dl.predict(df_scaled)[0][0]
    pred = int(pred_prob >= 0.5)
    return {"prediction": pred, "probability": float(pred_prob)}
