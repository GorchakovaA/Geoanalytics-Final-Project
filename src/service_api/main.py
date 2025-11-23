from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func # Импортируем func для использования функций PostGIS
from database import get_db, Meteorite
# Импортируем ST_AsText для конвертации геометрии в WKT-строку
from geoalchemy2.functions import ST_AsText 
# Импортируем BaseModel для создания схемы данных
from pydantic import BaseModel
# СХЕМА ДАННЫХ ДЛЯ ВХОДЯЩЕГО ЗАПРОСА (Body)
# Пользователь должен прислать эти поля.
class MeteoriteCreate(BaseModel):
    name: str
    recclass: str
    year: str | None = None  # Может быть пустым (None)
    mass: str | None = None
    reclat: float
    reclong: float

    # Pydantic Configuration
    class Config:
        # Разрешает использовать имена полей с пробелами, но в БД у нас уже 'mass (g)'
        # В данном случае это не строго необходимо, но полезно для сложных моделей
        orm_mode = True

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Сервис метеоритов работает"}

# Используем func.ST_AsText() для возврата геометрии в виде текста
def get_select_list():
    """Возвращает список колонок для SELECT-запроса, 
    конвертируя geom в WKT."""
    return [
        Meteorite.id,
        Meteorite.name,
        Meteorite.recclass,
        Meteorite.year,
        Meteorite.mass,
        Meteorite.reclat,
        Meteorite.reclong,
        # Используем ST_AsText для конвертации геометрии в строку WKT
        ST_AsText(Meteorite.geom).label("wkt_geometry") 
    ]

@app.get("/meteorites/all")
def get_all(db: Session = Depends(get_db)):
    data = db.query(*get_select_list()).all()
    # Результат — это список объектов SQLAlchemy. Преобразуем его в список словарей для чистого JSON.
    # Это важно, так как мы используем query(*select_list)
    return [
        {
            "id": row.id,
            "name": row.name,
            "recclass": row.recclass,
            "year": row.year,
            "mass (g)": row.mass,
            "reclat": row.reclat,
            "reclong": row.reclong,
            "geom": row.wkt_geometry # Поле теперь называется 'geom' и содержит WKT
        } 
        for row in data
    ]

@app.get("/meteorites/{limit}")
def get_with_limit(limit: int, db: Session = Depends(get_db)):
    # Используем ту же логику для лимитированных запросов
    data = db.query(*get_select_list()).limit(limit).all()
    return [
        {
            "id": row.id,
            "name": row.name,
            "recclass": row.recclass,
            "year": row.year,
            "mass (g)": row.mass,
            "reclat": row.reclat,
            "reclong": row.reclong,
            "geom": row.wkt_geometry
        } 
        for row in data
    ]
## 6. Создание POST-запроса
@app.post("/meteorites")
def create_meteorite(
    # Принимаем данные по схеме MeteoriteCreate
    new_meteorite: MeteoriteCreate, 
    db: Session = Depends(get_db)
):
    """
    Добавляет новую запись о метеорите в таблицу 'meteorites'.
    """
    try:
        # Создаем новый объект Meteorite, используя данные из запроса.
        # GeoAlchemy2 автоматически создаст POINT из reclat/reclong.
        # Мы используем ST_MakePoint из PostGIS для создания геометрии.
        db_meteorite = Meteorite(
            name=new_meteorite.name,
            recclass=new_meteorite.recclass,
            year=new_meteorite.year,
            mass=new_meteorite.mass, 
            reclat=new_meteorite.reclat,
            reclong=new_meteorite.reclong,
            # Создаем геометрию POINT из долготы и широты
            geom=func.ST_SetSRID(func.ST_MakePoint(new_meteorite.reclong, new_meteorite.reclat), 4326)
        )
        
        # Добавляем объект в сессию, выполняем INSERT и фиксируем изменения (commit)
        db.add(db_meteorite)
        db.commit()
        
        # Обновляем объект, чтобы получить его ID, присвоенный базой данных
        db.refresh(db_meteorite)
        
        return {"status": "success", "message": f"Метеорит {db_meteorite.name} успешно добавлен (ID: {db_meteorite.id})."}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Ошибка добавления данных: {e}"}
