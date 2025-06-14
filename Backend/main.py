from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data, plots, predict

app = FastAPI()

# Dodaj ovo CORS middleware
origins = [
    "http://localhost:5174",  # tvoj frontend port
    # možeš dodati i druge domene ako trebaš
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # dozvoli zahtjeve samo s ovih domena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/data", tags=["Data"])
app.include_router(plots.router, prefix="/plots", tags=["Plots"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

@app.get("/")
async def root():
    return {"message": "Learning Analytics Dashboard backend is running"}
