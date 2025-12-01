from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="client") # 'admin' o 'client'

    # Relación: Un usuario puede tener muchas reservas
    appointments = relationship("Appointment", back_populates="user")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # Ej: "Corte de Pelo"
    price = Column(Float)             # Ej: 15.00
    duration_minutes = Column(Integer) # Ej: 30

    # Relación: Un servicio está en muchas reservas
    appointments = relationship("Appointment", back_populates="service")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    appointment_date = Column(DateTime) # Fecha y hora del turno
    status = Column(String, default="pending") # pending, confirmed, cancelled

    # Relaciones inversas para poder acceder a los detalles
    user = relationship("User", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")