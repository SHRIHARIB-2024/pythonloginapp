from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pymysql
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    return pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME'],
        ssl={'ca': 'C:/Users/shrih/Downloads/DigiCertGlobalRootCA.crt.pem'}
    )

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return templates.TemplateResponse("welcome.html", {"request": request, "name": username})
    else:
        return HTMLResponse("Invalid credentials. Try again.", status_code=401)


# uvicorn app:app --host 0.0.0.0 --port 8001
