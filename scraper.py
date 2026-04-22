from fastapi import FastAPI, HTTPException
import sqlite3
import os
from datetime import datetime

app = FastAPI()


# 🧠 DB helper
def get_db(project: str):
    conn = sqlite3.connect(f"{project}.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


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


# 🟢 CREATE PROJECT (auto-create DB file)
@app.post("/project/create/{project}")
def create_project(project: str):
    conn = get_db(project)
    init_db(conn)
    return {"message": f"{project} created"}


# 🔴 DELETE PROJECT
@app.delete("/project/delete/{project}")
def delete_project(project: str):
    file = f"{project}.db"
    if os.path.exists(file):
        os.remove(file)
        return {"message": f"{project} deleted"}
    raise HTTPException(status_code=404, detail="Project not found")


# 🟡 ADD LEAD
@app.post("/leads/{project}")
def add_lead(project: str, data: dict):
    conn = get_db(project)
    init_db(conn)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO leads (company, website, score, created_at)
        VALUES (?, ?, ?, ?)
        """, (
            data["company"],
            data["website"],
            data["score"],
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        return {"message": f"added to {project}"}

    except sqlite3.IntegrityError:
        return {"error": "duplicate website"}


# 🔵 GET LEADS
@app.get("/leads/{project}")
def get_leads(project: str):
    conn = get_db(project)
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
