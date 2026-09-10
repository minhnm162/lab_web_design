from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "Frontend"


# Task 1: Prediction function
def predict_price(area: float, bedrooms: int, location: str) -> float:
    price = 500_000_000

    price += area * 15_000_000
    price += bedrooms * 50_000_000

    location = location.strip().lower()

    if location == "hanoi":
        price *= 1.3
    elif location == "hcmc":
        price *= 1.25

    # Round to the nearest million VND
    price = round(price / 1_000_000) * 1_000_000

    return float(price)


# Task 2: GET /predict
# We use def because this endpoint only performs simple synchronous calculations
# and does not need asynchronous I/O.
@app.get("/predict")
def get_prediction(
    area: float,
    bedrooms: int,
    location: str = "other"
):
    predicted_price = predict_price(area, bedrooms, location)

    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price
    }


# Task 6 Bonus: POST /predict
class HouseInput(BaseModel):
    area: float
    bedrooms: int
    location: str = "other"


@app.post("/predict")
def post_prediction(house: HouseInput):
    predicted_price = predict_price(
        house.area,
        house.bedrooms,
        house.location
    )

    return {
        "area": house.area,
        "bedrooms": house.bedrooms,
        "location": house.location,
        "predicted_price": predicted_price
    }


# Task 4: Serve frontend files
@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "house_form.html")


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)