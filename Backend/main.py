from pathlib import Path
import time
from uuid import uuid4

from fastapi import APIRouter, Cookie, Depends, FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)


class Item(ItemIn):
    id: int


class CartIn(BaseModel):
    item_id: int
    quantity: int = Field(ge=1)


app = FastAPI()
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

items = [Item(id=1, name="Book", price=50000), Item(id=2, name="Pen", price=5000)]
customers = [
    {"id": 1, "name": "An", "email": "an@example.com"},
    {"id": 2, "name": "Binh", "email": "binh@example.com"},
]
cart: list[dict] = []
sessions: dict[str, dict] = {}
next_id = 3


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    took = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(took)
    print(f"{request.method} {request.url.path} -> {response.status_code} ({took:.3f}s)")
    return response


def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    return {"skip": skip, "limit": limit}


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != "expected-secret":
        raise HTTPException(status_code=401, detail="Invalid API key")


def get_data():
    try:
        yield {"items": items, "customers": customers}
    finally:
        print("Session closed")


def get_session(response: Response, session_id: str | None = Cookie(default=None)):
    session_id = session_id or str(uuid4())
    sessions.setdefault(session_id, {})
    response.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return sessions[session_id]


def find_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


admin = APIRouter(prefix="/admin", dependencies=[Depends(verify_api_key)])


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/visits")
def visits(response: Response, visits: str | None = Cookie(default=None)):
    count = int(visits) + 1 if visits else 1
    response.set_cookie("visits", str(count), httponly=True, samesite="lax")
    return {"visits": count}


def set_login_cookie(response: Response):
    sessions.setdefault("abc123", {})
    response.set_cookie("session_id", "abc123", httponly=True, samesite="lax")
    return {"status": "logged in"}


@app.get("/login")
def login_get(response: Response):
    return set_login_cookie(response)


@app.post("/login")
def login_post(response: Response):
    return set_login_cookie(response)


@app.get("/set")
def set_session(session: dict = Depends(get_session)):
    session["user_id"] = 42
    return {"status": "set"}


@app.get("/session")
def read_session(session: dict = Depends(get_session)):
    return session


@app.get("/flash/set")
def set_flash(session: dict = Depends(get_session)):
    session["flash"] = "Item saved successfully"
    return {"status": "flash set"}


@app.get("/flash")
def read_flash(session: dict = Depends(get_session)):
    return {"message": session.pop("flash", None)}


@app.get("/customers")
def read_customers(page: dict = Depends(pagination), data: dict = Depends(get_data)):
    return data["customers"][page["skip"]:page["skip"] + page["limit"]]


@app.post("/card/add", status_code=201)
def add_cart(data: CartIn):
    item = find_item(data.item_id)
    row = next((row for row in cart if row["item_id"] == item.id), None)
    if row is None:
        row = {"item_id": item.id, "name": item.name, "price": item.price, "quantity": 0}
        cart.append(row)
    row["quantity"] += data.quantity
    row["total"] = row["price"] * row["quantity"]
    return row


@app.get("/cart")
def read_cart():
    return cart


@admin.get("/items/me")
def read_me():
    return "Welcome!"


@admin.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    return find_item(item_id)


@admin.get("/items", response_model=list[Item])
def read_items(
    page: dict = Depends(pagination),
    data: dict = Depends(get_data),
    q: str | None = Query(None, min_length=2),
):
    result = data["items"]
    if q:
        result = [item for item in result if q.lower() in item.name.lower()]
    return result[page["skip"]:page["skip"] + page["limit"]]


@admin.post("/items", response_model=Item, status_code=201)
def create_item(data: ItemIn):
    global next_id
    item = Item(id=next_id, name=data.name, price=data.price)
    items.append(item)
    next_id += 1
    return item


@admin.put("/items", response_model=Item)
def update_item(data: Item):
    item = find_item(data.id)
    item.name = data.name
    item.price = data.price
    return item


@admin.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    items.remove(find_item(item_id))


app.include_router(admin)
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
