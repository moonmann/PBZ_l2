from fastapi import FastAPI, Response, Query, Body, Depends, Request, Form
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json
from dateParser import parse_date
from DataBase import *
import random

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
    """for i in range(1, 6):
        a = WaterUseType(water_use_type=f"Водопользование_{i}")
        db.add(a)
    db.commit()
    a = db.query(WaterUseType).all()
    for i in a:
        db.delete(i)
    db.commit()
    for i in range(1, 16):
        a = Substance(substance_name=f"Вещество_{i}", 
                      danger_class=random.randint(1,5), 
                      lvf=random.randint(1,50), 
                      group=random.randint(1,10))
        db.add(a)
    db.commit()
    for i in range(1, 26):
        a = Drop(drop_name=f"Сброс_{i}",
                 diameter=random.randint(10, 50),
                 min_water_speed=random.randint(1, 50),
                 water_consumption=random.randint(1, 40),
                 date=f"{random.randint(1,28)}.{random.randint(1,12)}.{random.randint(2000,2023)}",
                 angel_about_water=random.randint(1, 90),
                 distance_to_water=random.randint(1, 100),
                 distance_to_coast=random.randint(1, 100)
                 )
        db.add(a)
    db.commit()
    for i in range(1, 16):
        a = Target(target_name=f"Створ_{i}",
                      drop_drop_name=f"Сброс_{random.randint(1, 25)}")
        db.add(a)
    db.commit()
    for i in range(1, 16):
        a = WaterUseTypeToSubstance(waterUseType_water_use_type=f"Водопользование_{random.randint(1, 5)}", 
                                    substance_substance_name=f"Вещество_{random.randint(1, 15)}")
        db.add(a)
    db.commit()
    for i in range(1, 26):
        a = SubstanceToDrop(substance_substance_name=f"Вещество_{random.randint(10, 15)}",
                            drop_drop_name=f"Сброс_{random.randint(10, 25)}",
                            concentration_in_drop=random.randint(1, 50),
                            concentration_in_target=random.randint(1, 50),
                            pdk=random.randint(1, 40),
                            knk=random.randint(1, 90)
                            )
        db.add(a)
    for i in range(1, 21):
        a = Factory(factory_name=f"Предприятие_{i}",
                    waterUseType_water_use_type=f"Водопользование_{random.randint(1, 5)}",
                    target_target_name=f"Створ_{random.randint(1, 15)}"
                    )
        db.add(a)
    db.commit()"""
    return db.query(Factory).all()


@app.post("/api/factories")
def create_factory(data=Body(), db: Session = Depends(get_db)):
    if db.query(Factory).filter(Factory.factory_name == data["factory_name"],
                                Factory.waterUseType_water_use_type == data["water_use_type"],
                                Factory.target_target_name == data["target_name"]).first():
        return JSONResponse(status_code=404, content={"message": "Такое предприятие уже существует"})
    if db.query(Factory).filter(Factory.factory_name == data["factory_name"],
                                Factory.target_target_name == data["target_name"]).first():
        return JSONResponse(status_code=404, content={"message": "Предприятие с водопользованием уже существует"})
    if not db.query(Target).filter(Target.target_name == data["target_name"]).all():
        return JSONResponse(status_code=404, content={"message": "Створа не существует"})
    if not db.query(WaterUseType).filter(WaterUseType.water_use_type == data["water_use_type"]).all():
        return JSONResponse(status_code=404, content={"message": "Типа водопользования не существует"})
    factory = Factory(factory_name=data["factory_name"],
                      waterUseType_water_use_type=data["water_use_type"],
                      target_target_name=data["target_name"])
    if db.query(Factory).filter(Factory.factory_name == data["factory_name"]).first().waterUseType_water_use_type != data["water_use_type"]:
        factories_to_update = db.query(Factory).filter(Factory.factory_name == data["factory_name"]).all()
        for i in factories_to_update:
            i.waterUseType_water_use_type = data["water_use_type"]
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
    factory_to_update = db.query(Factory).filter(Factory.factory_name == data["old_factory_name"],
                                                 Factory.target_target_name == data["old_target_name"],
                                                 Factory.waterUseType_water_use_type == data[
                                                     "old_water_use_type"]).first()
    if factory_to_update is None:
        return {"message": "Предприятие не найдено"}
    if db.query(Factory).filter(Factory.factory_name == data["old_factory_name"],
                                Factory.target_target_name == data["new_target_name"],
                                Factory.waterUseType_water_use_type == data["new_water_use_type"]).first():
        return JSONResponse(status_code=404, content={"message": "Такое предприятие уже существует"})
    if not db.query(WaterUseType).filter(WaterUseType.water_use_type == data["new_water_use_type"]).all():
        return JSONResponse(status_code=404, content={"message": "Типа водопользования не существует"})
    if not db.query(Target).filter(Target.target_name == data["new_target_name"]).all():
        return JSONResponse(status_code=404, content={"message": "Створа не существует"})
    if factory_to_update.waterUseType_water_use_type != data["new_water_use_type"]:
        factories_to_update = db.query(Factory).filter(Factory.factory_name == data["old_factory_name"]).all()
        for i in factories_to_update:
            i.waterUseType_water_use_type = data["new_water_use_type"]
    factory_to_update.target_target_name = data["new_target_name"]
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
    if not parse_date(data["date"]):
        return JSONResponse(status_code=404, content={"message": "Неправильный ввод даты"})
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
    delete_sub = db.query(SubstanceToDrop).filter(SubstanceToDrop.drop_drop_name == data["drop_name"]).all()
    for i in found_values:
        db.delete(i)
    if delete_sub:
        for i in delete_sub:
            db.delete(i)
    db.commit()
    return found_values


@app.post("/api/update_drops")
async def update_factory(data=Body(), db: Session = Depends(get_db)):
    drop = db.query(Drop).filter(Drop.idDrop == data["drop_id"]).first()
    if drop is None:
        return JSONResponse(status_code=404, content={"message": "Сброс с указанным ID не найден"})
    if len(db.query(Drop).filter(Drop.drop_name == data["drop_name"]).all()) > 1:
        return JSONResponse(status_code=404, content={"message": "Выпуск уже существует"})
    if not parse_date(data["date"]):
        return JSONResponse(status_code=404, content={"message": "Неправильный ввод даты"})
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
@app.get("/api/requests_subs")
def get_drop(db: Session = Depends(get_db)):
    time_table = db.query(SubstanceToDrop.idSubstanceToDrop,
                          SubstanceToDrop.substance_substance_name,
                          SubstanceToDrop.drop_drop_name,
                          SubstanceToDrop.concentration_in_drop).all()
    if not time_table:
        return JSONResponse(status_code=404, content={"message": "Ничего не найдено"})
    json_result = json.dumps([
        {
            'ID': row[0],
            'Название вещества': row[1],
            'Название сброса': row[2],
            'Концетрация в сбросе': row[3]
        }
        for row in time_table
    ])
    return json_result


@app.get("/api/requests_target")
def get_drop(db: Session = Depends(get_db)):
    time_table = db.query(SubstanceToDrop.idSubstanceToDrop, Target.target_name, SubstanceToDrop.drop_drop_name,
                          SubstanceToDrop.pdk, SubstanceToDrop.knk, SubstanceToDrop.concentration_in_target).join(
        Target,
        Target.drop_drop_name == SubstanceToDrop.drop_drop_name).all()
    if not time_table:
        return JSONResponse(status_code=404, content={"message": "Ничего не найдено"})
    json_result = json.dumps([
        {
            'ID': row[0],
            'Название створа': row[1],
            'Название сброса': row[2],
            'ПДК': row[3],
            'КНК': row[4],
            'Концетрация в створе': row[5]
        }
        for row in time_table
    ])
    return json_result


@app.post("/api/requests_drop")
def get_drop(data=Body(), db: Session = Depends(get_db)):
    if not db.query(Factory).filter(Factory.factory_name == data["factory_name"]).all():
        return JSONResponse(status_code=404, content={"message": "Предприятия не существует"})
    if not parse_date(data["date"]):
        return JSONResponse(status_code=404, content={"message": "Неправильный ввод даты"})
    if not db.query(Drop).filter(Drop.date == data["date"]).all():
        return JSONResponse(status_code=404, content={"message": "Сброса с такой датой не существует"})
    time_table = db.query(Factory.factory_name, Drop.drop_name, Drop.date) \
        .join(Target, Target.drop_drop_name == Drop.drop_name) \
        .join(Factory, Factory.target_target_name == Target.target_name) \
        .filter(Factory.factory_name == data["factory_name"], Drop.date == data["date"]) \
        .all()
    if not time_table:
        return JSONResponse(status_code=404, content={"message": "Ничего не найдено"})
    json_result = json.dumps([
        {
            'Название предприятия': row[0],
            'Название сброса': row[1],
            'Дата': row[2],
        }
        for row in time_table
    ])
    return json_result


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
