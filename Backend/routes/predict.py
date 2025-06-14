import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from model_utils import predict_rf, predict_dl
from typing import List
import random

router = APIRouter()

class StudentData(BaseModel):
    sex: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    math_percentage: float
    reading_score_percentage: float
    writing_score_percentage: float

@router.post("/predict")
async def predict(data: StudentData):
    input_data = data.dict()
    rf_pred = predict_rf(input_data)
    dl_pred = predict_dl(input_data)
    return {
        "random_forest_prediction": rf_pred,
        "deep_learning_prediction": dl_pred["prediction"],
        "deep_learning_probability": dl_pred["probability"]
    }

@router.get("/latest", response_model=List[dict])
async def latest_predictions():
    # Učitaj CSV (navedi stvarnu putanju do CSV datoteke)
    df = pd.read_csv("Student Performance new.csv")

    # Nasumično odaberi 10 studenata
    sample_df = df.sample(n=10, random_state=42)

    results = []
    for i, row in sample_df.iterrows():
        # Pretvori redak u dict i mapiraj nazive kolona na one koje StudentData očekuje
        student_dict = {
            "sex": row["sex"],
            "race_ethnicity": row["race/ethnicity"],
            "parental_level_of_education": row["parental level of education"],
            "lunch": row["lunch"],
            "test_preparation_course": row["test preparation course"],
            "math_percentage": row["math percentage"],
            "reading_score_percentage": row["reading score percentage"],
            "writing_score_percentage": row["writing score percentage"],
        }

        student = StudentData(**student_dict)
        pred = await predict(student)
        results.append({
            "id": i,
            **pred
        })

    return results
