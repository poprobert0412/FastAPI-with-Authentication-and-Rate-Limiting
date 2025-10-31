from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from typing import Dict, Any, Optional

# --- 1. SETĂRI ȘI BAZĂ DE DATE SIMULATĂ ---
# Baza de date
fake_db = {
    1: {"name": "First Job", "salary": 50000.0},
    2: {"name": "Second Job", "salary": 70000.0},
}
next_id = 3


# Model pentru creare (Payload)
class JobCreate(BaseModel):
    name: str
    salary: float


# --- 2. LOGICĂ DE SECURITATE (DEPENDENȚE) ---

# Cheie API Similată și Contor de Cereri (pentru Throttling)
VALID_API_KEY = "SECRET_KEY_123"
REQUEST_COUNTER: Dict[str, int] = {}  # Contorizam cererile per cheie


# Funcție de Autentificare (Authorization)
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Verifică dacă antetul X-API-Key este prezent și valid.
    Returnează 401 Unauthorized dacă eșuează.
    """
    if x_api_key != VALID_API_KEY:
        # 401 Unauthorized: Când autentificarea eșuează
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401 Unauthorized: Invalid API Key. Please provide a valid X-API-Key header."
        )
    return x_api_key  # Returnează cheia pentru Throttling


# Funcție de Limitare a Cérerilor (Throttling)
def rate_limit_per_key(api_key: str = Depends(verify_api_key)):
    """
    Simulează limitarea la un număr maxim de cereri (ex: 5 cereri).
    Returnează 429 Too Many Requests dacă limita e depășită.
    """
    MAX_REQUESTS = 5

    # Incrementăm contorul pentru cheia curentă
    REQUEST_COUNTER[api_key] = REQUEST_COUNTER.get(api_key, 0) + 1

    if REQUEST_COUNTER[api_key] > MAX_REQUESTS:
        # 429 Too Many Requests: Când limita de cereri e depășită
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"429 Too Many Requests: Rate limit exceeded. Max {MAX_REQUESTS} requests allowed."
        )
    # Rețineți: Acesta este un contor simplu care nu se resetează în timp.


# --- 3. INIȚIALIZARE ȘI ENDPOINTS (RUTE) ---

app = FastAPI()


# Endpoint care necesită Autentificare (API Key) ȘI Throttling
@app.get("/jobs/", status_code=status.HTTP_200_OK)
def read_all_jobs(auth_check: str = Depends(rate_limit_per_key)):
    """
    Afișează toate joburile. Necesită API Key și este supus la throttling.
    Cod de Retur: 200 OK.
    """
    return list(fake_db.values())


# Endpoint pentru Creare (POST)
@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, auth_check: str = Depends(verify_api_key)):
    """
    Creează un job nou. Necesită API Key, dar nu e limitat de throttling (pentru simplitate).
    Cod de Retur: 201 Created.
    """
    global next_id
    new_job_data = job.model_dump()

    # 409 Conflict: Simulare (opțional, pentru un scenariu mai complex)
    # if new_job_data["name"] == "Existing Job":
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Job with this name already exists.")

    fake_db[next_id] = new_job_data
    new_job_id = next_id
    next_id += 1

    # 201 Created: Succes în urma unei cereri POST
    return {"id": new_job_id, **new_job_data}


# Endpoint pentru Citire după ID (GET)
@app.get("/jobs/{job_id}", status_code=status.HTTP_200_OK)
def read_job(job_id: int, auth_check: str = Depends(verify_api_key)):
    """
    Afișează un job specific. Necesită API Key.
    Coduri de Retur: 200 OK sau 404 Not Found.
    """
    if job_id in fake_db:
        return fake_db[job_id]
    else:
        # 404 Not Found: Când resursa cerută nu există
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404 Not Found: Job ID {job_id} not found."
        )