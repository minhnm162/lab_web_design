# Mini House-Price Prediction API

## Run the project

Open PowerShell in the project root and run:

```powershell
cd Backend
python -m uvicorn main:app --reload
```

Then open the frontend at:

```text
http://127.0.0.1:8000/static/house_form.html
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Install the dependencies first when needed:

```powershell
python -m pip install -r requirements.txt
```

## API checks

For this request:

```text
GET /predict?area=80&bedrooms=3&location=hanoi
```

The response is:

```json
{
  "area": 80.0,
  "bedrooms": 3,
  "location": "hanoi",
  "predicted_price": 2405000000.0
}
```

The request can also be entered directly in the browser address bar:

```text
http://127.0.0.1:8000/predict?area=80&bedrooms=3&location=hanoi
```

`location` is optional because the endpoint gives it the default value `"other"` when it is omitted. `area` is required, so omitting it causes FastAPI to return HTTP `422` validation error.

## Frontend request

The form uses `fetch('/predict?...')` with a relative URL. This works because FastAPI serves the frontend and the API from the same origin: `127.0.0.1:8000`. The browser therefore sends the request to the same host and port without a CORS configuration.

The form displays the returned `predicted_price` with thousands separators and shows an error message when the request fails.

## Bonus POST endpoint

The optional POST endpoint accepts JSON instead of query parameters:

```json
{
  "area": 80,
  "bedrooms": 3,
  "location": "hanoi"
}
```

Query parameters are sent in the URL, while a JSON body is sent inside the HTTP request body.
