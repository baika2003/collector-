from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timezone
from pathlib import Path
import json
import base64

app = FastAPI(
    title="Collector Server",
    description="Centralized Log Collection System",
    version="0.1.0"
)

RAW_DIR = Path("storage/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = RAW_DIR / "events.jsonl"


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "collector-server"
    }


@app.post("/ingest")
async def ingest(request: Request):
    try:
        raw_data = await request.body()

        if not raw_data:
            raise HTTPException(
                status_code=400,
                detail="Empty log event"
            )

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": request.client.host if request.client else None,
            "raw": raw_data.decode("utf-8", errors="replace"),
            "raw_base64": base64.b64encode(raw_data).decode("ascii")
        }

        with RAW_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

        return {
            "status": "accepted",
            "message": "Log successfully stored"
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to store log event"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
