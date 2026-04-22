import requests

BASE = "https://insta-api-5g7b.onrender.com"

# -------------------------
# CREATE PROJECT
# -------------------------
def create_project(name):
    return requests.post(f"{BASE}/project/create/{name}").json()

# -------------------------
# ADD LEAD
# -------------------------
def add_lead(project, company, website, score):
    data = {
        "company": company,
        "website": website,
        "score": score
    }
    return requests.post(f"{BASE}/leads/{project}", json=data).json()

# -------------------------
# GET LEADS
# -------------------------
def get_leads(project):
    return requests.get(f"{BASE}/leads/{project}").json()

# -------------------------
# DELETE LEAD
# -------------------------
def delete_lead(project, lead_id):
    return requests.delete(f"{BASE}/leads/{project}/{lead_id}").json()

# -------------------------
# UPDATE LEAD
# -------------------------
def update_lead(project, lead_id, company, website, score):
    data = {
        "company": company,
        "website": website,
        "score": score
    }
    return requests.put(f"{BASE}/leads/{project}/{lead_id}", json=data).json()

# -------------------------
# EXPORT DATABASE (DOWNLOAD)
# -------------------------
def download_db(project):
    r = requests.get(f"{BASE}/export/{project}")

    if r.status_code == 200:
        with open(f"{project}.db", "wb") as f:
            f.write(r.content)
        return "Downloaded"
    return r.text


# =========================
# TEST RUN
# =========================
print(create_project("project1"))
print(add_lead("project1", "OpenAI", "https://openai.com", 99))
print(get_leads("project1"))
print(download_db("project1"))