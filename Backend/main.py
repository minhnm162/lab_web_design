from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float


class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


_items: list[ItemPublic] = []
_next_id = 1


def _find(item_id: int) -> ItemPublic | None:
    for item in _items:
        if item.id == item_id:
            return item

    return None


def _has_same_name(name: str, item_id: int | None = None) -> bool:
    for item in _items:
        if item_id is not None and item.id == item_id:
            continue

        if item.name.lower() == name.lower():
            return True

    return False


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="../frontend", html=True),
    name="static"
)


@app.get("/items/me")
def read_me():
    return "Welcome!"


# GET AN ITEM
@app.get("/items/{item_id}", response_model=ItemPublic)
def read_item(item_id: int):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# GET ITEMS
@app.get("/items", response_model=ItemListResponse)
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(None, min_length=2),
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str = Query("id", pattern="^(id|name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$")
):
    result = _items

    if q is not None:
        result = [
            item for item in result
            if q.lower() in item.name.lower()
        ]

    if min_price is not None:
        result = [
            item for item in result
            if item.price >= min_price
        ]

    if max_price is not None:
        result = [
            item for item in result
            if item.price <= max_price
        ]

    total = len(result)

    result = sorted(
        result,
        key=lambda item: getattr(item, sort_by),
        reverse=order == "desc"
    )

    return ItemListResponse(
        items=result[skip:skip + limit],
        total=total,
        skip=skip,
        limit=limit
    )


# CREATE AN ITEM
@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global _next_id

    if _has_same_name(data.name):
        raise HTTPException(
            status_code=409,
            detail="Item with this name already exists"
        )

    newItem = ItemPublic(
        id=_next_id,
        name=data.name,
        price=data.price
    )

    _items.append(newItem)
    _next_id += 1

    return newItem


# UPDATE AN ITEM
@app.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, data: ItemCreate):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    if data.name.lower() != item.name.lower() and _has_same_name(data.name, item.id):
        raise HTTPException(
            status_code=409,
            detail="Item with this name already exists"
        )

    updateValue = ItemPublic(
        id=item.id,
        name=data.name,
        price=data.price
    )

    index = _items.index(item)
    _items[index] = updateValue

    return updateValue


# PATCH AN ITEM
@app.patch("/items/{item_id}", response_model=ItemPublic)
def patch_item(item_id: int, data: ItemUpdate):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    updateData = data.model_dump(exclude_unset=True)

    if "name" in updateData and updateData["name"] is None:
        raise HTTPException(
            status_code=422,
            detail="Name cannot be null"
        )

    if "price" in updateData and updateData["price"] is None:
        raise HTTPException(
            status_code=422,
            detail="Price cannot be null"
        )

    if "name" in updateData:
        if updateData["name"].lower() != item.name.lower() and _has_same_name(updateData["name"], item.id):
            raise HTTPException(
                status_code=409,
                detail="Item with this name already exists"
            )

    updateValue = ItemPublic(
        id=item.id,
        name=updateData.get("name", item.name),
        price=updateData.get("price", item.price)
    )

    index = _items.index(item)
    _items[index] = updateValue

    return updateValue


# DELETE AN ITEM
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = _find(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    _items.remove(item)

    return None


# PREDICT HOUSE PRICE
@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(data: HousePriceRequest):
    predictedPrice = (
        data.area_sqm * 15000000
        - data.distance_to_center_km * 5000000
        + data.bedrooms * 20000000
    )

    return HousePricePrediction(predicted_price=predictedPrice)
