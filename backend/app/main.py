from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests

extension_version = "1.0"
chrome_id = "chrome-extension://bmhegdpjmmogcajlaiijjhonljofhegh"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[chrome_id],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# structure of the packet we expect to recieve from frontend
class CapturePacket(BaseModel):
    version: str
    highlight: str
    paragraph: str
    title: str
    url: str
    timestamp: datetime
    # highlight length: int. <--- add later
    # paragraph length: int  <--- add later

@app.get("/")
def root():
    return {"status": "backend running"}

query_text = ""
@app.post("/capture")
def receive_capture(packet: CapturePacket):
    # sanity check
    print("Received capture packet:", packet.model_dump())
    query_text = packet.highlight.strip()
    papers = search_crossref(query_text)

    return {
    "query": query_text,
    "papers": papers
}

# call the semantic scholar api 

def search_crossref(query_text):
    url = "https://api.crossref.org/works"

    params = {
        "query": query_text,
        "rows": 5
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Crossref error:", response.status_code)
        return []

    data = response.json()

    items = data.get("message", {}).get("items", [])

    papers = []

    for item in items:
        title_list = item.get("title", [])
        title = title_list[0] if title_list else "Untitled"

        year = None
        issued = item.get("issued", {})
        date_parts = issued.get("date-parts", [])
        if date_parts and len(date_parts[0]) > 0:
            year = date_parts[0][0]

        doi = item.get("DOI")
        url = f"https://doi.org/{doi}" if doi else item.get("URL")

        papers.append({
            "title": title,
            "year": year,
            "url": url
        })

    return papers

# packet
# vector database


# top 3 articles with a simialrty score URL that you can press and title of the article.

# list of articles, each article has a title, URL, and similarity score. The user can click on the URL to read the article.
