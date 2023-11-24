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
    return FileResponse('public/index.html')


# region Files
@app.get("/api/factories")
def get_factory():
    return FileResponse("public/factory.html")


@app.get("/api/drops")
def get_factory():
    return FileResponse("public/drop.html")


@app.get("/api/requests")
def get_factory():
    return FileResponse("public/requests.html")


@app.get("/api/tables")
def get_factory():
    return FileResponse("public/tables.html")


# endregion


# region Factory
@app.get("/api/factory")
def get_factory(db: Session = Depends(get_db)):
    return db.query(Factory).all()


@app.post("/api/factories")
def create_factory(data=Body(), db: Session = Depends(get_db)):
    if db.query(Factory).filter(Factory.factory_name == data["factory_name"]).all():
        return JSONResponse(status_code=404, content={"message": "Предприятие уже существует"})
    factory = Factory(factory_name=data["factory_name"],
                      waterUseType_idWaterUseType=data["water_use_type"],
                      target_idTarget=data["target_id"])
    db.add(factory)
    db.commit()
    db.refresh(factory)
    return factory


@app.delete("/api/factories")
def delete_factory(data=Body(), db: Session = Depends(get_db)):
    found_values = db.query(Factory).filter(Factory.factory_name == data["factory_name"]).all()
    if not found_values:
        return JSONResponse(status_code=404, content={"message": "Предприятие не найдено"})
    for i in found_values:
        db.delete(i)
    db.commit()
    return found_values


@app.post("/api/update_factories")
async def update_factory(data=Body(), db: Session = Depends(get_db)):
    factory_to_update = db.query(Factory).filter(Factory.idFactory == data["factory_id"]).first()
    if factory_to_update is None:
        return {"message": "Фабрика с указанным ID не найдена"}
    factory_to_update.factory_name = data["factory_name"]
    factory_to_update.waterUseType_idWaterUseType = data["water_use_type"]
    factory_to_update.target_idTarget = data["target_id"]
    db.commit()
    return factory_to_update


# endregion


# region Drop
@app.get("/api/drop")
def get_drop(db: Session = Depends(get_db)):
    return db.query(Drop).all()


@app.post("/api/drops")
def create_drop(data=Body(), db: Session = Depends(get_db)):
    drop = Drop(drop_name=data["drop_name"], diameter=data["diameter"],
                min_water_speed=data["min_water_speed"], water_consumption=data["water_consumption"],
                angel_about_water=data["angel_about_water"], distance_to_water=data["distance_to_water"],
                distance_to_coast=data["distance_to_coast"], date=data["date"])
    if db.query(Drop).filter(Drop.drop_name == drop.drop_name).all():
        return JSONResponse(status_code=404, content={"message": "Выпуск уже существует"})
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


@app.delete("/api/drops")
def delete_drop(data=Body(), db: Session = Depends(get_db)):
    found_values = db.query(Drop).filter(Drop.drop_name == data["drop_name"]).all()
    if not found_values:
        return JSONResponse(status_code=404, content={"message": "Сброс не найден"})
    for i in found_values:
        db.delete(i)
    db.commit()
    return found_values


@app.post("/api/update_drops")
async def update_factory(data=Body(), db: Session = Depends(get_db)):
    drop = db.query(Drop).filter(Drop.idDrop == data["drop_id"]).first()
    if drop is None:
        return JSONResponse(status_code=404, content={"message": "Сброс с указанным ID не найден"})
    drop.drop_name = data["drop_name"]
    drop.diameter = data["diameter"]
    drop.min_water_speed = data["min_water_speed"]
    drop.water_consumption = data["water_consumption"]
    drop.angel_about_water = data["angel_about_water"]
    drop.distance_to_water = data["distance_to_water"]
    drop.distance_to_coast = data["distance_to_coast"]
    drop.date = data["date"]
    db.commit()
    return {"message": "Сброс успешно обновлен"}


# endregion


# region Requests

# endregion


# region Tables
@app.get("/api/target")
def get_drop(db: Session = Depends(get_db)):
    return db.query(Target).all()


@app.get("/api/substance")
def get_drop(db: Session = Depends(get_db)):
    return db.query(Substance).all()


@app.get("/api/water_use_type")
def get_drop(db: Session = Depends(get_db)):
    return db.query(WaterUseType).all()


@app.get("/api/water_use_type_to_substance")
def get_drop(db: Session = Depends(get_db)):
    return db.query(WaterUseTypeToSubstance).all()


@app.get("/api/substance_to_drop")
def get_drop(db: Session = Depends(get_db)):
    return db.query(SubstanceToDrop).all()

# endregion
