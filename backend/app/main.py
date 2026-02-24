from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/capture")
def receive_capture(packet: CapturePacket):
    # sanity check
    print("Received capture packet:", packet.model_dump())
    return {"status": "received", "chars": len(packet.highlight)}


# packet
# vector database


# top 3 articles with a simialrty score URL that you can press and title of the article.

# list of articles, each article has a title, URL, and similarity score. The user can click on the URL to read the article.
