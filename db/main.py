from fastapi import FastAPI, Depends, Body
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship, joinedload
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import enum
import json
import os

DATABASE_URL = "sqlite:///./armstrim.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/v_video", StaticFiles(directory=os.path.join(BASE_DIR, "test1_video")), name="v_video")
app.mount("/v_fire", StaticFiles(directory=os.path.join(BASE_DIR, "test2_fire")), name="v_fire")
app.mount("/v_guard", StaticFiles(directory=os.path.join(BASE_DIR, "test3_guard")), name="v_guard")
app.mount("/v_tex", StaticFiles(directory=os.path.join(BASE_DIR, "test4_tex")), name="v_tex")
app.mount("/img", StaticFiles(directory=os.path.join(BASE_DIR, "img")), name="img")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    TECHNICIAN = "technician"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="manager")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    services = relationship("Service", back_populates="category")

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    services = relationship("Service", back_populates="brand")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price_per_unit = Column(Float)
    unit_name = Column(String)
    image = Column(String, default="default.jpg")
    difficulty_factor = Column(Float, default=1.0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    
    category = relationship("Category", back_populates="services")
    brand = relationship("Brand", back_populates="services")
    specs = relationship("ServiceSpec", back_populates="service", cascade="all, delete-orphan")

class ServiceSpec(Base):
    __tablename__ = "service_specs"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    spec_name = Column(String)
    spec_value = Column(String)
    service = relationship("Service", back_populates="specs")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    client_phone = Column(String)
    details = Column(Text) 
    total_price = Column(Numeric(10, 2))
    quiz_data = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/", response_class=FileResponse)
def get_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/admin", response_class=FileResponse)
def get_admin():
    return FileResponse(os.path.join(BASE_DIR, "admin/admin.html"))

@app.get("/video", response_class=FileResponse)
def get_test_video():
    return FileResponse(os.path.join(BASE_DIR, "test1_video/index.html"))

@app.get("/fire", response_class=FileResponse)
def get_test_fire():
    return FileResponse(os.path.join(BASE_DIR, "test2_fire/index.html"))

@app.get("/guard", response_class=FileResponse)
def get_test_guard():
    return FileResponse(os.path.join(BASE_DIR, "test3_guard/index.html"))

@app.get("/tex", response_class=FileResponse)
def get_test_tex():
    return FileResponse(os.path.join(BASE_DIR, "test4_tex/index.html"))

@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).options(
        joinedload(Service.brand),
        joinedload(Service.category),
        joinedload(Service.specs)
    ).all()
    
    output = []
    for s in services:
        output.append({
            "id": s.id,
            "name": s.name,
            "price": float(s.price_per_unit),
            "unit": s.unit_name,
            "image": s.image,
            "difficulty_factor": s.difficulty_factor,
            "category_id": s.category_id,
            "category_name": s.category.name if s.category else "Общее",
            "brand": s.brand.name if s.brand else "Без бренда",
            "specs": [{"name": spec.spec_name, "value": spec.spec_value} for spec in s.specs]
        })
    return output

@app.get("/api/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.id.desc()).all()

@app.post("/api/orders")
def create_order(data: dict = Body(...), db: Session = Depends(get_db)):
    new_order = Order(
        client_phone=data.get("client_phone"),
        total_price=data.get("total_price", 0),
        details=data.get("details", ""),
        quiz_data=json.dumps(data.get("quiz_data")) if data.get("quiz_data") else None
    )
    db.add(new_order)
    db.commit()
    return {"status": "ok"}

@app.delete("/api/orders/{o_id}")
def delete_order(o_id: int, db: Session = Depends(get_db)):
    db.query(Order).filter(Order.id == o_id).delete()
    db.commit()
    return {"status": "deleted"}

@app.post("/api/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    user = db.query(User).filter(User.username == username).first()
    if user and user.hashed_password == password:
        return {
            "status": "success", 
            "user": {
                "username": user.username, 
                "role": user.role
            }
        }
    return {"status": "error", "message": "Неверный логин или пароль"}