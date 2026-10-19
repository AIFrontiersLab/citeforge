"""Tests for Research MVP."""
import pytest
from httpx import AsyncClient, ASGITransport
from main import app, decompose_query, parse_and_synthesize, SynthesisResult

client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)

class TestDecomposeQuery:
    def test_simple_query(self):
        res = decompose_query("machine learning")
        assert len(res) == 1
        assert res[0] == "machine learning"

    def test_complex_query(self):
        res = decompose_query("machine learning and deep learning")
        assert len(res) == 2
        assert "machine learning" in res
        assert "deep learning" in res

class TestParseAndSynthesize:
    def test_empty_input(self):
        brief = parse_and_synthesize([], [])
        assert brief.topic == "Unknown"
        assert brief.summary == "Research on 'Unknown' yielded 0 key points."

    def test_with_data(self):
        subs = ["machine learning"]
        data = [{"content": "machine learning", "point": "ML is cool."}]
        res = parse_and_synthesize(subs, data)
        assert res.topic == "machine learning"
        assert len(res.key_points) == 1
        assert "ML is cool." in res.key_points

class TestAPIEndpoints:
    @pytest.mark.asyncio
    async def test_simple_research(self):
        resp = await client.post("/research", json={"query": "machine learning"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["topic"] == "machine learning"

    @pytest.mark.asyncio
    async def test_empty_query_error(self):
        # FastAPI returns 422 for validation error (min_length=1)
        resp = await client.post("/research", json={"query": ""})
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_json(self):
        resp = await client.post("/research", content="not json", headers={"content-type": "application/json"})
        assert resp.status_code == 422