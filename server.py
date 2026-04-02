from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
import jwt, bcrypt, os
from typing import Optional, List

app = FastAPI(title="Albadent CRM API")
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-in-prod")
security = HTTPBearer()

# ✅ Modelos
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    role: str = "RECEPTIONIST"  # ADMIN, RECEPTIONIST, DENTIST_1, DENTIST_2

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PatientCreate(BaseModel):
    fullName: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    medicalHistory: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(BaseModel):
    patientId: str
    dentistId: Optional[str] = None
    date: datetime
    reason: str  # revision, limpieza, urgencia, estetica, ortodoncia, implantes
    notes: Optional[str] = None
    status: str = "PENDING"  # PENDING, CONFIRMED, COMPLETED, CANCELLED

class PaymentCreate(BaseModel):
    patientId: str
    amount: float
    description: str
    paymentDate: datetime = Field(default_factory=datetime.utcnow)

# ✅ Auth
@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    # Verificar usuario en DB (placeholder)
    if credentials.email == "admin@albadent.com" and credentials.password == "admin123":
        token = jwt.encode({
            "sub": "admin-id",
            "email": credentials.email,
            "role": "ADMIN",
            "exp": datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return {"token": token, "user": {"email": credentials.email, "role": "ADMIN"}}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/api/auth/google")
async def google_auth(code: str):
    # Implementar flujo OAuth2 de Google
    pass

# ✅ Pacientes
@app.post("/api/patients", status_code=201)
async def create_patient(patient: PatientCreate, creds: HTTPAuthorizationCredentials = Depends(security)):
    # Verificar token y permisos
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    if payload["role"] not in ["ADMIN", "RECEPTIONIST"]:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # Crear paciente en DB (placeholder)
    return {"id": "patient-123", **patient.dict(), "createdAt": datetime.utcnow()}

@app.get("/api/patients")
async def list_patients(search: Optional[str] = None, creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    # Query con filtro de búsqueda
    return [{"id": "p1", "fullName": "Isabel Rodríguez", "phone": "612345678", "email": "isabel@email.com"}]

# ✅ Citas
@app.post("/api/appointments", status_code=201)
async def create_appointment(appt: AppointmentCreate, creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    # Crear cita con validación de horarios
    return {"id": "appt-456", **appt.dict()}

@app.get("/api/appointments")
async def list_appointments(status_filter: Optional[str] = None, date_from: Optional[str] = None, creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    # Filtrar por estado/fecha/rol
    return [
        {
            "id": "a1",
            "patient": {"fullName": "Isabel Rodríguez Torres"},
            "status": "CONFIRMED",
            "reason": "Limpieza dental",
            "dentist": "Dr. García",
            "date": "2026-03-27T17:00:00"
        },
        {
            "id": "a2",
            "patient": {"fullName": "María López García"},
            "status": "CONFIRMED",
            "reason": "Revisión general",
            "dentist": "Dr. García",
            "date": "2026-03-28T11:00:00"
        }
    ]

@app.patch("/api/appointments/{id}")
async def update_appointment(id: str, status: str, creds: HTTPAuthorizationCredentials = Depends(security)):
    # Actualizar estado de cita
    return {"id": id, "status": status, "updatedAt": datetime.utcnow()}

@app.delete("/api/appointments/{id}")
async def delete_appointment(id: str, creds: HTTPAuthorizationCredentials = Depends(security)):
    # Eliminar cita (soft delete recomendado)
    return {"success": True}

# ✅ Pagos
@app.post("/api/payments", status_code=201)
async def create_payment(payment: PaymentCreate, creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    # Registrar pago
    return {"id": "pay-789", **payment.dict()}

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
    # Calcular KPIs
    return {
        "totalBilled": 15420.50,
        "totalPaid": 12300.00,
        "pending": 3120.50,
        "appointmentsToday": 8,
        "pendingAppointments": 12
    }

# ✅ Reserva pública (sin auth)
@app.post("/api/public/appointments", status_code=201)
async def public_booking(appt: AppointmentCreate):
    # Validar datos básicos
    if appt.reason not in ["revision", "limpieza", "urgencia", "estetica", "ortodoncia", "implantes"]:
        raise HTTPException(status_code=400, detail="Motivo no válido")
    
    # Guardar en cola de revisión (no confirma automáticamente)
    return {"success": True, "message": "Solicitud recibida. Te contactaremos para confirmar."}
