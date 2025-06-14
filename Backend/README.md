#  Learning Analytics Dashboard – Backend

Ovaj projekt predstavlja FastAPI backend za analizu studentskih podataka. Omogućuje upload CSV datoteka, generiranje statistika i grafova te predikciju prolaznosti studenata pomoću Random Forest i Deep Learning modela.

## Pokretanje projekta

python -m venv venv
venv\Scripts\activate

## Instalacija ovisnosti 

pip install -r requirements.txt

## Pokretanje FastAPI 

uvicorn main:app --reload
