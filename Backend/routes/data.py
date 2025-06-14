from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io
import shared 

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    shared.uploaded_df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    stats = shared.uploaded_df.describe().to_dict()
    return {"stats": stats}

@router.get("/data-summary")
async def data_summary():
    if shared.uploaded_df is None:
        return {"error": "No data uploaded"}
    sample = shared.uploaded_df.head(10).to_dict(orient="records")
    stats = shared.uploaded_df.describe().to_dict()
    return {"sample": sample, "statistics": stats}

@router.get("/statistics")
async def statistics():
    if shared.uploaded_df is None:
        return {"error": "No data uploaded"}
    # Dohvati prvih 10 studenata za prikaz
    students = shared.uploaded_df.head(10).to_dict(orient="records")

    # Izračunaj prosjek za potrebna polja, prilagodi nazive kolona prema stvarnom CSV-u
    avg_math = shared.uploaded_df['math percentage'].mean()
    avg_reading = shared.uploaded_df['reading score percentage'].mean()
    avg_writing = shared.uploaded_df['writing score percentage'].mean()

    return {
        "students": students,
        "avg_math": avg_math,
        "avg_reading": avg_reading,
        "avg_writing": avg_writing
    }
