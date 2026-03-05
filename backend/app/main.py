from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import requests
import keyword_search

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
    papers = keyword_search.find_papers(query_text) # calling openalex search 
    ranked_papers = '' # vector embedding

    return {
    "query": query_text,
    "papers": papers
}