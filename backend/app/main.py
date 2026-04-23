from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, usuarios, cursos, horarios, inscripciones, asistencias, calificaciones, certificados, encuestas, docentes, estudiantes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LASIN API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(cursos.router)
app.include_router(horarios.router)
app.include_router(inscripciones.router)
app.include_router(asistencias.router)
app.include_router(calificaciones.router)
app.include_router(certificados.router)
app.include_router(encuestas.router)
app.include_router(docentes.router)
app.include_router(estudiantes.router)

@app.get("/")
def root():
    return {"message": "LASIN API corriendo correctamente ✅"}