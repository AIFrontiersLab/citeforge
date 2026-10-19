"""Minimal Research Synthesis MVP."""
import re
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Research MVP")

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)

class SynthesisResult(BaseModel):
    topic: str
    summary: str
    key_points: List[str]

def decompose_query(query: str) -> List[str]:
    """Split query into sub-questions."""
    query = query.strip().lower()
    if not query:
        return []
    # Simple heuristic: split on 'and', 'or', 'vs'
    parts = re.split(r'\s+(?:and|or|vs)\s+', query)
    return [p.strip() for p in parts if p.strip()]

def parse_and_synthesize(sub_queries: List[str], mock_data: List[Dict[str, Any]]) -> SynthesisResult:
    """Synthesize results from mock data."""
    if not sub_queries:
        return SynthesisResult(
            topic="Unknown",
            summary="Research on 'Unknown' yielded 0 key points.",
            key_points=[]
        )
    topic = sub_queries[0]
    points = []
    for sub in sub_queries:
        for item in mock_data:
            if sub in item.get("content", "").lower():
                points.append(item.get("point", ""))
    summary = f"Research on '{topic}' yielded {len(points)} key points."
    return SynthesisResult(topic=topic, summary=summary, key_points=points)

@app.post("/research", response_model=SynthesisResult)
def research(request: QueryRequest):
    sub_queries = decompose_query(request.query)
    # Mock data for demonstration
    mock_data = [
        {"content": "machine learning", "point": "ML automates tasks."},
        {"content": "deep learning", "point": "DL uses neural nets."},
        {"content": "data science", "point": "DS analyzes data."}
    ]
    result = parse_and_synthesize(sub_queries, mock_data)
    return result

def demo():
    """Run a demo synthesis."""
    q = "machine learning and deep learning"
    subs = decompose_query(q)
    res = parse_and_synthesize(subs, [
        {"content": "machine learning", "point": "ML automates tasks."},
        {"content": "deep learning", "point": "DL uses neural nets."}
    ])
    print(f"Topic: {res.topic}")
    print(f"Summary: {res.summary}")
    print(f"Points: {res.key_points}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)