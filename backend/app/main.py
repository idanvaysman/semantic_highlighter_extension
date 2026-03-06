from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# local imports
import keyword_search
from rank_papers import embedding_model

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
class RankRequest(BaseModel):
    query: str
    papers: list[dict]

@app.get("/")
def root():
    return {"status": "backend running"}

query_text = ""
@app.post("/search")
def receive_capture(packet: CapturePacket):
    # sanity check
    print("Received capture packet:", packet.model_dump())
    query_text = packet.highlight.strip()
    papers = keyword_search.find_papers(query_text) # calling openalex search 
    #rank_papers = embedding_model(query_text, 3).rank_papers(papers) # calling embedding model to rank papers by relevance to query text.

    return {
    "query": query_text,
    "papers": papers
}

@app.post("/rank")
def receive_rank(data: RankRequest):
    # You access data like an object
    rank_papers = embedding_model(data.query, 3).rank_papers(data.papers) # calling embedding model to rank papers by relevance to query text.
    return {
    "query": data.query,
    "papers": rank_papers
    }

