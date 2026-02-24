from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests

#TO WORK ON: FINISH EMBEDDING FUNCTION AND VECTOR DATABASE, 
# THEN IMPLEMENT THE EMBEDDING SEARCH IN THE /capture ENDPOINT.

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
    papers = search_openalex(query_text)

    return {
    "query": query_text,
    "papers": papers
}

# call the openalex api 

def search_openalex(query_text):
    url = "https://api.openalex.org/works"

    params = {
        "search": query_text,
        "per-page": 30
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("OpenAlex error:", response.status_code)
        return []

    results = response.json().get("results", [])

    return [normalize_openalex_paper(item) for item in results]

# normalize the openalex response to include the title, URL (doi or PDF), and publication year.

def normalize_openalex_paper(item):
    title = item.get("display_name", "Untitled")
    year = item.get("publication_year")

    doi = item.get("doi")
    doi_url = f"https://doi.org/{doi}" if doi else None

    abstract = reconstruct_abstract(item.get("abstract_inverted_index"))

    is_oa = item.get("open_access", {}).get("is_oa", False)

    pdf_url = (
        item.get("primary_location", {}) or {}
    ).get("pdf_url")

    final_url = build_access_url(
        doi_url=doi_url,
        is_open_access=is_oa,
        pdf_url=pdf_url
    )

    return { # each one of these is an item in the papers list that we send back to the frontend
        "title": title,
        "year": year,
        "abstract": abstract,
        "url": final_url,
        "is_open_access": is_oa
    }

# the url prefix is the authentication for college access. 
# If the paper is open access, we can link directly to the PDF. 
# If not, we link to the DOI URL with the OpenAthens prefix for UCL access.

URL_PREFIX = "https://go.openathens.net/redirector/ucsc.edu?url=" #athenizer prefix for UCSC access

def build_access_url(doi_url, is_open_access, pdf_url=None):
    if is_open_access and pdf_url:
        return pdf_url

    if doi_url:
        return URL_PREFIX + doi_url

    return None

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return None

    max_pos = max(
        pos
        for positions in inverted_index.values()
        for pos in positions
    )

    words = [""] * (max_pos + 1)

    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word

    return " ".join(words)



def embedding_search(query_text):
    # call the embedding model to get the query embedding
    # query_embedding = get_embedding(query_text)
    pass 

# packet
# vector database


# top 3 articles with a simialrty score URL that you can press and title of the article.

# list of articles, each article has a title, URL, and similarity score. The user can click on the URL to read the article.
