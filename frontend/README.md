# Learning Analytics Dashboard - Frontend

Ovaj frontend projekt izrađen je u Vue 3 koristeći Vuetify kao UI framework. Prikazuje predikcije prolaznosti studenata na temelju modela strojog učenja (Random Forest i Deep Learning). 

## Opis projekta

- Prikazuje tablicu s podacima za 10 studenata, uključujući njihove karakteristike i predikcije prolaznosti.
- Izračunava maksimalnu i minimalnu vjerojatnost predikcije Deep Learning modela.
- Prikazuje grafički prikaz usporedbe predikcija dvaju modela koristeći Chart.js.
- Podaci se dohvaćaju sa backend API-ja (FastAPI) lokalno na `http://localhost:8000`.

## Tehnologije

- Vue 3 (Composition API)
- Vuetify 3
- Axios (za HTTP pozive)
- Chart.js (za grafikone)

## Instalacija
npm run dev
