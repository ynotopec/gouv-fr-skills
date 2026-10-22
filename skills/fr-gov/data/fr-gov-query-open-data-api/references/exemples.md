# Exemples rapides

```python
import requests

BASE = "https://www.data.gouv.fr/api/1"

# 1) Search catalog, then open first hit
r = requests.get(f"{BASE}/datasets/", params={"q": "transport", "page_size": 5}).json()
first = r["data"][0]
ds = requests.get(f"{BASE}/datasets/{first['id']}/").json()

# 2) Pick a CSV resource UUID, then Tabular profile + data (use any resource id exposed by Tabular)
csvs = [res for res in ds["resources"] if res.get("format", "").lower() == "csv"]
rid = csvs[0]["id"] if csvs else ds["resources"][0]["id"]
requests.get(f"https://tabular-api.data.gouv.fr/api/resources/{rid}/profile/").json()
requests.get(
    f"https://tabular-api.data.gouv.fr/api/resources/{rid}/data/",
    params={"page": 1, "page_size": 20},
).json()

# 3) Direct file download (when you need the raw file, not row filtering)
url = next(res["url"] for res in ds["resources"] if res["id"] == rid)
requests.get(url, stream=True)
```

```python
# Metrics API — paginated dataset metrics (models/columns in Swagger)
# ⚠️ modèle au PLURIEL : datasets, organizations, resources (pas dataset/organization/resource)
requests.get(
    "https://metric-api.data.gouv.fr/api/datasets/data/",
    params={"page": 1, "page_size": 20},
).json()
```

**Python client:** https://github.com/etalab/datagouv-client-python

---

