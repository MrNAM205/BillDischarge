
from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.TrustCorpusAgent import list_corpus_entries, add_entry

router = APIRouter()

class CorpusEntry(BaseModel):
    title: str
    content: str

@router.get("/trust/corpus")
def get_corpus():
    return { "entries": list_corpus_entries() }

@router.post("/trust/corpus/add")
def add_to_corpus(entry: CorpusEntry):
    added = add_entry(entry.title, entry.content)
    return { "entry": added }
