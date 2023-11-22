from fastapi import FastAPI, Response, Query, Body, Depends, Request, Form
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from DataBase import *

"""uvicorn WebApp:app --reload  """

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def main():
    return FileResponse('./public/index.html')


@app.get("/api/factory")
def get_factory(db: Session = Depends(get_db)):

    return db.query(Factory).all()


@app.post("/api/factory")
def create_factory(data=Body(), db: Session = Depends(get_db)):
    factory = Factory(factory_name=data["factory_name"], water_use_type=data["water_use_type"])
    if db.query(Factory).filter(Factory.factory_name == factory.factory_name).all():
        return JSONResponse(status_code=404, content={"message": "Предприятие уже существует"})
    db.add(factory)
    db.commit()
    db.refresh(factory)
    return factory


@app.get("/delete_factory")
async def delete(query1: str, db: Session = Depends(get_db)):
    found_values = db.query(Factory).filter(Factory.factory_name == query1).all()
    return {"query1": query1, "found_values1": found_values}


@app.delete("/api/factory")
def delete_factory(data=Body(), db: Session = Depends(get_db)):
    found_values = db.query(Factory).filter(Factory.factory_name == data["factory_name"]).all()
    if not found_values:
        return JSONResponse(status_code=404, content={"message": "Предприятие не найдено"})
    for i in found_values:
        db.delete(i)
    db.commit()
    return found_values


@app.post("/api/update_factory")
async def update_factory(data=Body(), db: Session = Depends(get_db)):
    factory_to_update = db.query(Factory).filter(Factory.id == data["factory_id"]).first()
    if factory_to_update is None:
        return {"message": "Фабрика с указанным ID не найдена"}
    factory_to_update.factory_name = data["factory_name"]
    factory_to_update.water_use_type = data["water_use_type"]
    db.commit()
    return {"message": "Фабрика успешно обновлена"}


@app.get("/api/drop")
def get_drop(db: Session = Depends(get_db)):
    return db.query(Drop).all()


@app.post("/api/drop")
def create_drop(data=Body(), db: Session = Depends(get_db)):
    drop = Drop(drop_name=data["drop_name"], diameter=data["diameter"],
                min_water_speed=data["min_water_speed"], water_consumption=data["water_consumption"],
                angle_about_water=data["angle_about_water"], distance_to_surface=data["distance_to_surface"],
                distance_to_coast=data["distance_to_coast"], date=data["date"])
    if db.query(Drop).filter(Drop.drop_name == drop.drop_name).all():
        return JSONResponse(status_code=404, content={"message": "Выпуск уже существует"})
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


@app.get("/delete_drop")
async def delete(query2: str, db: Session = Depends(get_db)):
    found_values = db.query(Drop).filter(Drop.drop_name == query2).all()
    return {"query2": query2, "found_values2": found_values}


@app.delete("/api/drop")
def delete_drop(data=Body(), db: Session = Depends(get_db)):
    found_values = db.query(Drop).filter(Drop.drop_name == data["drop_name"]).all()
    if not found_values:
        return JSONResponse(status_code=404, content={"message": "Сброс не найден"})
    for i in found_values:
        db.delete(i)
    db.commit()
    return found_values


@app.post("/api/update_drop")
async def update_factory(data=Body(), db: Session = Depends(get_db)):
    drop = db.query(Drop).filter(Drop.id == data["drop_id"]).first()
    if drop is None:
        return JSONResponse(status_code=404, content={"message": "Сброс с указанным ID не найден"})
    drop.drop_name = data["drop_name"]
    drop.diameter = data["diameter"]
    drop.min_water_speed = data["min_water_speed"]
    drop.water_consumption = data["water_consumption"]
    drop.angle_about_water = data["angle_about_water"]
    drop.distance_to_surface = data["distance_to_surface"]
    drop.distance_to_coast = data["distance_to_coast"]
    drop.date = data["date"]
    db.commit()
    return {"message": "Сброс успешно обновлен"}


@app.get("/api/target")
def get_target(db: Session = Depends(get_db)):
    return db.query(Target).all()


@app.get("/api/factory_to_drop")
def get_factory_to_drop(db: Session = Depends(get_db)):
    return db.query(FactoryToDrop).all()


@app.get("/api/drop_to_target")
def get_drop_to_target(db: Session = Depends(get_db)):
    return db.query(DropToTarget).all()


@app.post("/api/drop_to_target")
def create_drop_to_target(data=Body(), db: Session = Depends(get_db)):
    drop_to_target = DropToTarget(target_id=data["target_id"], drop_id=data["drop_id"], distance=data["distance"])
    if db.query(DropToTarget).filter(DropToTarget.drop_id == drop_to_target.drop_id).all():
        return JSONResponse(status_code=404, content={"message": "Выпуск уже имеет створ"})
    db.add(drop_to_target)
    db.commit()
    db.refresh(drop_to_target)
    return drop_to_target


@app.get("/delete_drop_to_target")
async def delete(query3: int, query4: int, db: Session = Depends(get_db)):
    found_values = db.query(DropToTarget).filter(
        and_(DropToTarget.drop_id == query4, DropToTarget.target_id == query3)).all()
    return {"query3": query3, "query4": query4, "found_values3": found_values}


@app.delete("/api/drop_to_target")
def delete_drop_to_target(data=Body(), db: Session = Depends(get_db)):
    found_values = db.query(DropToTarget).filter(DropToTarget.drop_id == data["drop_id"],
                                                 DropToTarget.target_id == data["target_id"]).all()
    if not found_values:
        return JSONResponse(status_code=404, content={"message": "Дистанция не найдена"})
    for i in found_values:
        db.delete(i)
    db.commit()
    return found_values


@app.get("/api/substance")
def get_substance(db: Session = Depends(get_db)):
    return db.query(Substance).all()


@app.get("/api/water_use_type_to_danger_class")
def get_water_use_type_to_danger_class(db: Session = Depends(get_db)):
    return db.query(WaterUseTypeToDangerClass).all()


@app.get("/api/water_use_type_to_lvf")
def get_water_use_type_to_lvf(db: Session = Depends(get_db)):
    return db.query(WaterUseTypeToLvf).all()


@app.get("/api/substance_to_drop")
def get_substance_to_drop(db: Session = Depends(get_db)):
    return db.query(SubstanceToDrop).all()
