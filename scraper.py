from fastapi import FastAPI, HTTPException
import sqlite3
import os
from datetime import datetime

app = FastAPI()


# =========================
# DB HELPERS
# =========================

def get_db(project: str):
    conn = sqlite3.connect(f"{project}.db", check_same_thread=False)
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


# =========================
# PROJECT CONTROL
# =========================

@app.post("/project/create/{project}")
def create_project(project: str):
    conn = get_db(project)
    init_db(conn)
    conn.close()
    return {"message": f"{project} created"}


@app.delete("/project/delete/{project}")
def delete_project(project: str):
    file = f"{project}.db"
    if os.path.exists(file):
        os.remove(file)
        return {"message": f"{project} deleted"}
    raise HTTPException(status_code=404, detail="Project not found")


@app.get("/projects")
def list_projects():
    files = [f.replace(".db", "") for f in os.listdir() if f.endswith(".db")]
    return {"projects": files}


# =========================
# LEAD CONTROL
# =========================

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
        conn.close()
        return {"message": "lead added"}

    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "duplicate website"}


@app.get("/leads/{project}")
def get_leads(project: str):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")
    rows = cursor.fetchall()
    conn.close()

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


@app.delete("/leads/{project}/{lead_id}")
def delete_lead(project: str, lead_id: int):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {"message": f"lead {lead_id} deleted"}


@app.put("/leads/{project}/{lead_id}")
def update_lead(project: str, lead_id: int, data: dict):
    conn = get_db(project)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE leads
    SET company = ?, website = ?, score = ?
    WHERE id = ?
    """, (
        data["company"],
        data["website"],
        data["score"],
        lead_id
    ))

    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Lead not found")

    return {"message": f"lead {lead_id} updated"}
