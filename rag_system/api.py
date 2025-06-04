from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from db import ChromaVectorDB

app = FastAPI(title="RAG System API")

# 전역 DB 인스턴스
db = ChromaVectorDB()

class Document(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    metadata_filter: Optional[Dict] = None

@app.get("/")
def root():
    return {"message": "RAG System API"}

@app.get("/stats")
def get_stats():
    """DB 통계 조회"""
    return db.get_stats()

@app.post("/documents")
def add_documents(documents: List[Document]):
    """문서 추가"""
    try:
        docs = [doc.dict() for doc in documents]
        success = db.add_documents(docs)
        if success:
            return {"message": f"{len(documents)}개 문서 추가 성공"}
        else:
            raise HTTPException(status_code=500, detail="문서 추가 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search_documents(request: SearchRequest):
    """문서 검색"""
    try:
        results = db.search(
            query=request.query,
            top_k=request.top_k,
            where=request.metadata_filter
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents")
def delete_documents(ids: List[str]):
    """문서 삭제"""
    try:
        success = db.delete_documents(ids)
        if success:
            return {"message": f"{len(ids)}개 문서 삭제 성공"}
        else:
            raise HTTPException(status_code=500, detail="문서 삭제 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 