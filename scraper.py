import requests

BASE = "https://insta-api-5g7b.onrender.com"

# =========================
# PROJECT
# =========================

def create_project(project):
    return requests.post(f"{BASE}/project/create/{project}").json()

def delete_project(project):
    return requests.delete(f"{BASE}/project/delete/{project}").json()

def list_projects():
    return requests.get(f"{BASE}/projects").json()

# =========================
# LEADS
# =========================

def add_lead(project, company, website, score):
    return requests.post(
        f"{BASE}/leads/{project}",
        json={
            "company": company,
            "website": website,
            "score": score
        }
    ).json()

def get_leads(project):
    return requests.get(f"{BASE}/leads/{project}").json()

def delete_lead(project, lead_id):
    return requests.delete(f"{BASE}/leads/{project}/{lead_id}").json()

def update_lead(project, lead_id, company, website, score):
    return requests.put(
        f"{BASE}/leads/{project}/{lead_id}",
        json={
            "company": company,
            "website": website,
            "score": score
        }
    ).json()

# =========================
# EXPORT
# =========================

def download_db(project):
    r = requests.get(f"{BASE}/export/{project}")

    if r.status_code == 200:
        with open(f"{project}.db", "wb") as f:
            f.write(r.content)
        return "downloaded"
    return r.text


# =========================
# TEST
# =========================

print(create_project("project1"))
print(add_lead("project1", "OpenAI", "https://openai.com", 99))
print(get_leads("project1"))
print(download_db("project1"))