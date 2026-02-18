from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import utils
from app.llm import summarize_diff
from app.database import SessionLocal, engine
from app import models, crud
from app.crawler import fetch_page_text
from sqlalchemy import text

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Competitive Intelligence Tracker")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok", "backend": "running"}

@app.post("/competitors")
def add_competitor(
    name: str,
    url: str,
    tags: str = "",
    db: Session = Depends(get_db)
):
    return crud.create_competitor(db, name, url, tags)
@app.get("/competitors")
def list_competitors(db: Session = Depends(get_db)):
    return db.query(models.Competitor).all()


@app.post("/check/{competitor_id}")
def check_competitor(
    competitor_id: int,
    db: Session = Depends(get_db)
):
    competitor = crud.get_competitor(db, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    new_text = fetch_page_text(competitor.url)
    last_snapshot = crud.get_last_snapshot(db, competitor_id)

    new_snapshot = crud.create_snapshot(db, competitor_id, new_text)

    # First snapshot
    if not last_snapshot:
        return {
            "message": "Initial snapshot stored",
            "snapshot_id": new_snapshot.id
        }

    # No change
    if last_snapshot.content_hash == new_snapshot.content_hash:
        return {
            "message": "No changes detected"
        }

    # Generate diff
    diff_text = utils.generate_diff(
        last_snapshot.content_text,
        new_snapshot.content_text
    )

    diff = crud.create_diff(
        db,
        competitor_id,
        last_snapshot.id,
        new_snapshot.id,
        diff_text
    )

    
    summary = summarize_diff(diff_text)

    crud.update_diff_summary(db, diff.id, summary)

    return {
        "message": "Changes detected",
        "diff_id": diff.id,
        "summary": summary
    }

@app.get("/history/{competitor_id}")
def competitor_history(
    competitor_id: int,
    db: Session = Depends(get_db)
):
    competitor = crud.get_competitor(db, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    diffs = crud.get_last_diffs(db, competitor_id)

    return {
        "competitor": {
            "id": competitor.id,
            "name": competitor.name,
            "url": competitor.url,
            "tags": competitor.tags,
        },
        "history": [
            {
                "diff_id": d.id,
                "created_at": d.created_at,
                "summary": d.summary,
            }
            for d in diffs
        ]
    }
@app.get("/status")
def status(db: Session = Depends(get_db)):
    # DB check
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # LLM check
    try:
        from app.llm import client
        llm_status = "ok"
    except Exception as e:
        llm_status = f"error: {str(e)}"

    return {
        "backend": "ok",
        "database": db_status,
        "llm": llm_status
    }
