from sqlalchemy.orm import Session
from models import CarCreate, CarRead, CarUpdate, Car
from database import SessionLocal


def _create_car(payload: CarCreate) -> CarRead:
    db = SessionLocal()
    try:
        car = Car(
            brand=payload.brand,
            model=payload.model,
            year=payload.year
        )
        db.add(car)
        db.commit()
        db.refresh(car)
        return CarRead.from_orm(car)
    except Exception as e:
        db.rollback()
        print(f"Error creating car: {e}")
        raise
    finally:
        db.close()


def _get_car_by_id(cid: int) -> CarRead:
    db = SessionLocal()
    try:
        car = db.query(Car).filter(Car.id == cid).first()
        if car:
            return CarRead.from_orm(car)
        return None
    finally:
        db.close()


def _delete_car(cid: int) -> bool:
    db = SessionLocal()
    try:
        car = db.query(Car).filter(Car.id == cid).first()
        if car:
            db.delete(car)
            db.commit()
            return True
        return False
    finally:
        db.close()


def _list_cars() -> list[CarRead]:
    db = SessionLocal()
    try:
        cars = db.query(Car).all()
        return [CarRead.from_orm(car) for car in cars]
    finally:
        db.close()


def _patch_car(cid: int, payload: CarUpdate) -> CarRead:
    db = SessionLocal()
    try:
        car = db.query(Car).filter(Car.id == cid).first()
        if not car:
            return None
        
        car.brand = payload.brand
        car.model = payload.model
        car.year = payload.year
        
        db.commit()
        db.refresh(car)
        return CarRead.from_orm(car)
    finally:
        db.close()


def _replace_car(cid: int, payload: CarCreate) -> CarRead:
    db = SessionLocal()
    try:
        car = db.query(Car).filter(Car.id == cid).first()
        if not car:
            return None
        
        car.brand = payload.brand
        car.model = payload.model
        car.year = payload.year
        
        db.commit()
        db.refresh(car)
        return CarRead.from_orm(car)
    finally:
        db.close()