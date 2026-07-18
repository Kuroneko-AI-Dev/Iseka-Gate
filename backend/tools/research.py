"""Controlled web-research capability for Aoi."""

from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
import os
from gpt_service import ask_gpt
import requests
from fastapi import HTTPException



TAVILY_SEARCH_URL = "https://api.tavily.com/search"
MAX_REQUESTS_PER_MINUTE = 5
_research_requests: dict[int, deque[datetime]] = defaultdict(deque)


def _enforce_rate_limit(user_id: int) -> None:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=1)
    requests_for_user = _research_requests[user_id]
    while requests_for_user and requests_for_user[0] < cutoff:
        requests_for_user.popleft()
    if len(requests_for_user) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(429, "Batas research tercapai. Coba lagi dalam satu menit.")
    requests_for_user.append(now)


def _search_web(query: str, max_results: int) -> list[dict[str, str]]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise HTTPException(503, "Web research belum dikonfigurasi. Tambahkan TAVILY_API_KEY di backend/.env.")
    try:
        response = requests.post(
            TAVILY_SEARCH_URL,
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": False,
                "include_raw_content": False,
            },
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(502, "Provider web research tidak dapat dihubungi.") from exc

    sources = []
    for item in response.json().get("results", [])[:max_results]:
        if item.get("url"):
            sources.append({
                "title": item.get("title", "Sumber tanpa judul")[:200],
                "url": item["url"],
                "snippet": item.get("content", "")[:1200],
            })
    return sources



def research(query: str, user_id: int, max_results: int = 5):
    
    #print("QUERY MASUK KE TAVILY =", query)
    _enforce_rate_limit(user_id)

    query = f"{query} terbaru hari ini"

    sources = _search_web(
        query,
        max_results
    )

    return {
        "sources": sources
    }

def summarize_research(query, sources):

    source_text = ""

    for index, source in enumerate(sources, start=1):

        source_text += (
            f"[{index}] {source['title']}\n"
            f"{source['snippet']}\n\n"
        )


    prompt = f"""
Kamu adalah mesin peringkas informasi.

Pertanyaan:
{query}

Data sumber:

{source_text}

Tugas:
- Buat ringkasan fakta penting.
- Jangan menambahkan informasi yang tidak ada.
- Ambil angka/tanggal/nama penting jika tersedia.
- Gunakan Bahasa Indonesia.
- Maksimal 5 paragraf.
"""


    result = ask_gpt([
        {
            "role":"user",
            "content":prompt
        }
    ])


    return result