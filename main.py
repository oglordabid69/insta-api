from fastapi import FastAPI, HTTPException
import sqlite3
from datetime import datetime

app = FastAPI()


# 🧠 FUNCTION: get database per project
def get_db(project: str):
    conn = sqlite3.connect(f"{project}.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


# 🧠 FUNCTION: create table if not exists
def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        website TEXT UNIQUE,
        score INTEGER,
        created_at TEXT
    )
    """)
    conn.commit()


# 🟢 HOME
@app.get("/")
def home():
    return {"status": "Multi-project API is live 🚀"}


# 🔵 GET LEADS FOR A PROJECT
@app.get("/leads/{project}")
def get_leads(project: str):
    conn = get_db(project)
    init_db(conn)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "company": r[1],
            "website": r[2],
            "score": r[3],
            "created_at": r[4]
        }
        for r in rows
    ]


# 🟡 ADD LEAD TO A PROJECT
@app.post("/leads/{project}")
def add_lead(project: str, data: dict):
    conn = get_db(project)
    init_db(conn)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO leads (company, website, score, created_at) VALUES (?, ?, ?, ?)",
            (
                data["company"],
                data["website"],
                data["score"],
                datetime.utcnow().isoformat()
            )
        )
        conn.commit()
        return {"message": f"added to {project}"}

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate website")


# 🔴 DELETE LEAD
@app.delete("/leads/{project}/{lead_id}")
def delete_lead(project: str, lead_id: int):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()

    return {"message": f"deleted {lead_id} from {project}"}


# 🟢 FILTER
@app.get("/leads/{project}/filter")
def filter_leads(project: str, min_score: int = 0):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE score >= ?",
        (min_score,)
    )
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "company": r[1],
            "website": r[2],
            "score": r[3],
            "created_at": r[4]
        }
        for r in rows
    ]


# 🔍 SEARCH
@app.get("/leads/{project}/search")
def search_leads(project: str, query: str):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE company LIKE ?",
        (f"%{query}%",)
    )
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "company": r[1],
            "website": r[2],
            "score": r[3],
            "created_at": r[4]
        }
        for r in rows
    ]