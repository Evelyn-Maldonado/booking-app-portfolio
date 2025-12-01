from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas # <--- Importamos los esquemas nuevos
from database import engine, get_db

# Crea las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Endpoint para crear Servicios (Usando Schemas) ---
@app.post("/services/", response_model=schemas.ServiceResponse)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    new_service = models.Service(
        name=service.name, 
        price=service.price, 
        duration_minutes=service.duration_minutes
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# --- Endpoint para crear Usuarios (Rápido para probar) ---
@app.post("/users/")
def create_user(email: str, db: Session = Depends(get_db)):
    new_user = models.User(email=email, role="client")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- EL CORAZÓN DEL SISTEMA: Crear Reserva ---
@app.post("/appointments/", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # 1. Validar que el servicio exista
    service = db.query(models.Service).filter(models.Service.id == appointment.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # 2. LÓGICA DE NEGOCIO: ¿Ya existe un turno a esa hora para ese servicio?
    # Buscamos en la BD si hay algo con el mismo service_id y la misma fecha
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.service_id == appointment.service_id,
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.status != "cancelled" # Ignoramos los cancelados
    ).first()

    if existing_appointment:
        # Si existe, devolvemos error 400 (Bad Request) o 409 (Conflict)
        raise HTTPException(status_code=409, detail="Este horario ya está ocupado")

    # 3. Si está libre, guardamos
    new_appointment = models.Appointment(
        user_id=appointment.user_id,
        service_id=appointment.service_id,
        appointment_date=appointment.appointment_date
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment