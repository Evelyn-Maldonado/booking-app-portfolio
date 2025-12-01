from pydantic import BaseModel
from datetime import datetime

# Esquema para crear un Servicio (lo que envía el usuario)
class ServiceCreate(BaseModel):
    name: str
    price: float
    duration_minutes: int

# Esquema para responder (incluye el ID que genera la BD)
class ServiceResponse(ServiceCreate):
    id: int
    class Config:
        from_attributes = True

# Esquema para crear una Reserva
class AppointmentCreate(BaseModel):
    user_id: int
    service_id: int
    appointment_date: datetime # FastAPI validará que sea una fecha real

# Esquema para responder la Reserva
class AppointmentResponse(AppointmentCreate):
    id: int
    status: str
    class Config:
        from_attributes = True