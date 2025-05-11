from fastapi import FastAPI, Request, Form, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pyodbc
from starlette.status import HTTP_302_FOUND

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# SQL Server connection string
conn_str = (
    "Driver={SQL Server};"
    "Server=MINH\\SQLEXPRESS;"
    "Database=VideoGameDb;"
    "Trusted_Connection=yes;"
)

# ------------------------
# Route: Trang chủ
# ------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VideoGames")
        games = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "games": games})

# ------------------------
# Route: Thêm game
# ------------------------
@app.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
def create_game(title: str = Form(...), platform: str = Form(...),
                developer: str = Form(...), publisher: str = Form(...)):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO VideoGames (Title, Platform, Developer, Publisher)
            VALUES (?, ?, ?, ?)
        """, (title, platform, developer, publisher))
        conn.commit()
    return RedirectResponse("/", status_code=HTTP_302_FOUND)

# ------------------------
# Route: Cập nhật
# ------------------------
@app.get("/update/{game_id}", response_class=HTMLResponse)
def update_form(request: Request, game_id: int):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VideoGames WHERE Id = ?", (game_id,))
        game = cursor.fetchone()
    return templates.TemplateResponse("update.html", {"request": request, "game": game})

@app.post("/update/{game_id}")
def update_game(game_id: int, title: str = Form(...), platform: str = Form(...),
                developer: str = Form(...), publisher: str = Form(...)):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE VideoGames SET Title = ?, Platform = ?, Developer = ?, Publisher = ?
            WHERE Id = ?
        """, (title, platform, developer, publisher, game_id))
        conn.commit()
    return RedirectResponse("/", status_code=HTTP_302_FOUND)

# ------------------------
# Route: Xoá game
# ------------------------
@app.get("/delete/{game_id}")
def delete_game(game_id: int):
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM VideoGames WHERE Id = ?", (game_id,))
        conn.commit()
    return RedirectResponse("/", status_code=HTTP_302_FOUND)
