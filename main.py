from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List

app = FastAPI()


# Модели Pydantic
class MushroomCreate(BaseModel):
    name: str
    edible: bool
    weight: int
    freshness: int = Field(ge=0, le=10, description="Свежесть гриба от 0 до 10")  # Изменено на int с валидацией


class Mushroom(MushroomCreate):
    id: int


class BasketCreate(BaseModel):
    owner: str
    capacity: int


class Basket(BaseModel):
    id: int
    owner: str
    capacity: int
    mushrooms: List[int] = []


class BasketResponse(BaseModel):
    id: int
    owner: str
    capacity: int
    mushrooms: List[Mushroom]


# "База данных" в памяти
db = {
    "mushrooms": {},
    "baskets": {},
    "next_mushroom_id": 1,
    "next_basket_id": 1,
}


# Эндпоинты для грибов
@app.post("/mushrooms/", response_model=Mushroom)
def create_mushroom(mushroom: MushroomCreate):
    mushroom_id = db["next_mushroom_id"]
    db["mushrooms"][mushroom_id] = Mushroom(id=mushroom_id, **mushroom.dict())
    db["next_mushroom_id"] += 1
    return db["mushrooms"][mushroom_id]


@app.put("/mushrooms/{mushroom_id}", response_model=Mushroom)
def update_mushroom(mushroom_id: int, mushroom: MushroomCreate):
    if mushroom_id not in db["mushrooms"]:
        raise HTTPException(status_code=404, detail="Mushroom not found")
    db["mushrooms"][mushroom_id] = Mushroom(id=mushroom_id, **mushroom.dict())
    return db["mushrooms"][mushroom_id]


@app.get("/mushrooms/{mushroom_id}", response_model=Mushroom)
def get_mushroom(mushroom_id: int):
    if mushroom_id not in db["mushrooms"]:
        raise HTTPException(status_code=404, detail="Mushroom not found")
    return db["mushrooms"][mushroom_id]


# Эндпоинты для корзинок
@app.post("/baskets/", response_model=Basket)
def create_basket(basket: BasketCreate):
    basket_id = db["next_basket_id"]
    db["baskets"][basket_id] = Basket(id=basket_id, **basket.dict())
    db["next_basket_id"] += 1
    return db["baskets"][basket_id]


@app.post("/baskets/{basket_id}/add")
def add_mushroom_to_basket(basket_id: int, mushroom_id: int):
    basket = db["baskets"].get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    mushroom = db["mushrooms"].get(mushroom_id)
    if not mushroom:
        raise HTTPException(status_code=404, detail="Mushroom not found")

    if mushroom_id in basket.mushrooms:
        raise HTTPException(status_code=400, detail="Mushroom already in basket")

    total_weight = sum(m.weight for m in [db["mushrooms"][mid] for mid in basket.mushrooms])
    if total_weight + mushroom.weight > basket.capacity:
        raise HTTPException(status_code=400, detail="Basket capacity exceeded")

    basket.mushrooms.append(mushroom_id)
    return {"message": "Mushroom added successfully"}


@app.delete("/baskets/{basket_id}/remove")
def remove_mushroom_from_basket(basket_id: int, mushroom_id: int):
    basket = db["baskets"].get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    if mushroom_id not in basket.mushrooms:
        raise HTTPException(status_code=404, detail="Mushroom not in basket")

    basket.mushrooms.remove(mushroom_id)
    return {"message": "Mushroom removed successfully"}


@app.get("/mushrooms/", response_model=List[Mushroom])
def get_mushrooms():
    return list(db["mushrooms"].values())


@app.get("/baskets/", response_model=List[Basket])
def get_baskets():
    return list(db["baskets"].values())


@app.get("/baskets/{basket_id}", response_model=BasketResponse)
def get_basket(basket_id: int):
    basket = db["baskets"].get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    mushrooms = [db["mushrooms"][mid] for mid in basket.mushrooms if mid in db["mushrooms"]]
    return BasketResponse(
        id=basket.id,
        owner=basket.owner,
        capacity=basket.capacity,
        mushrooms=mushrooms
    )