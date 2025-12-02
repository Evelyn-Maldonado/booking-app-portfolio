from pydantic import BaseModel
from datetime import datetime

# 1. Base: Datos comunes que siempre están
class UserBase(BaseModel):
    email: str

# 2. Input: Lo que el usuario envía para registrarse
# AQUÍ es donde definimos que la contraseña es OBLIGATORIA
class UserCreate(UserBase):
    password: str   # <--- ¡Esta es la línea clave que hará aparecer el campo!
    role: str = "client" # Opcional, por defecto es cliente

# 3. Output: Lo que la API responde al frontend
# IMPORTANTE: Aquí NO ponemos el password para no devolverlo en el JSON
class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    
    class Config:
        from_attributes = True


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