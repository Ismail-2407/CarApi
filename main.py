from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import CarRead, CarCreate
from car_repository_service import _create_car, _get_car_by_id, _delete_car, _list_cars
from database import create_tables

create_tables()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola de Mundo!!!!"}


@app.post('/cars', response_model=CarRead, status_code=201)
def create_car(payload: CarCreate):
    return _create_car(payload)

@app.get('/cars', response_model=List[CarRead])
def get_all_cars(brand: Optional[str] = None,
    model: Optional[str] = None,
    limit: int = 100,
    offset: int = 0):
    items = _list_cars()
    if brand:
        items = [c for c in items if brand.lower() in c.brand.lower()]
    if model:
        items = [c for c in items if model.lower() in c.model.lower()]
    offset = max(offset, 0) * max(limit, 1)
    return items[offset : offset + limit]


@app.get('/cars/{id}', response_model=CarRead)
def get_car(id: int):
    car = _get_car_by_id(id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.delete('/cars/{id}', status_code=204)
def delete_car(id: int):
    deleted = _delete_car(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return None


