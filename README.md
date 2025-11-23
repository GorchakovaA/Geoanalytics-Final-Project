# Geoanalytics-Final-Project
Итоговый проект по геоаналитике, демонстрирующий полный цикл обработки пространственных данных: от Python/PostGIS до RESTful-сервиса на FastAPI.
# Финальный проект по дисциплине: Геоаналитика и обработка пространственных данных

**Автор:** Горчакова А.П.
**Полный отчет:** [Скачать PDF](./Gorchakova_Final_Report.pdf)

## О проекте

Проект демонстрирует полный цикл работы с геопространственными данными: от очистки сырых данных и загрузки их в PostGIS до аналитики и создания веб-сервиса (API).

**Исходные данные:**
* [Meteorite_Landings.csv](./data/Meteorite_Landings.csv) — данные о падении метеоритов.
* [countries.geojson](./data/countries.geojson) — полигоны границ стран.

---

## Этапы реализации (Модули)

### Модуль 1: Первичная обработка данных
**Файл:** [`src/01_data_prep_docker.ipynb`](./src/01_data_prep_docker.ipynb)

Первичная очистка данных в среде Docker/Jupyter. Удаление записей с отсутствующими координатами, приведение типов и создание интерактивной карты визуализации падений.

### Модуль 2: Работа с PostGIS и GeoPandas
**Файл:** [`src/02_postgis_geopandas.ipynb`](./src/02_postgis_geopandas.ipynb)

Загрузка геоданных в базу PostGIS. Демонстрация работы с библиотекой GeoPandas для чтения данных из БД и выполнения пространственных соединений (Spatial Join) для определения страны падения метеорита.

### Модуль 3: SQL-запросы через Python
**Файл:** [`src/03_sql_queries.ipynb`](./src/03_sql_queries.ipynb)

Выполнение сложных SQL-запросов к PostGIS через SQLAlchemy:
* Пространственный поиск (`ST_Contains`)
* Временной анализ (фильтрация по годам)
* Агрегация данных и фильтрация по массе.

### Модуль 4: Геосервис на FastAPI
**Папка:** [`src/service_api/`](./src/service_api/)

Реализация REST API сервиса.
* `database.py` — конфигурация подключения к БД и ORM-модели (GeoAlchemy2).
* `main.py` — эндпоинты API (GET для получения списка с WKT-геометрией, POST для добавления точек).

---

## Запуск проекта

1. **База данных:** Требуется запущенный контейнер Docker с PostGIS.
2. **Зависимости:** `pip install pandas geopandas sqlalchemy geoalchemy2 fastapi uvicorn psycopg2-binary`
3. **Запуск API:**
   ```bash
   uvicorn src.service_api.main:app --reload
