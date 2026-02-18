import hashlib
from sqlalchemy.orm import Session
from app import models
from app.models import DiffResult

def create_competitor(db: Session, name: str, url: str, tags: str = ""):
    competitor = models.Competitor(
        name=name,
        url=url,
        tags=tags
    )
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor


def get_competitor(db: Session, competitor_id: int):
    return db.query(models.Competitor).filter(models.Competitor.id == competitor_id).first()


def get_last_snapshot(db: Session, competitor_id: int):
    return (
        db.query(models.Snapshot)
        .filter(models.Snapshot.competitor_id == competitor_id)
        .order_by(models.Snapshot.created_at.desc())
        .first()
    )


def create_snapshot(db: Session, competitor_id: int, content_text: str):
    content_hash = hashlib.sha256(content_text.encode()).hexdigest()

    snapshot = models.Snapshot(
        competitor_id=competitor_id,
        content_text=content_text,
        content_hash=content_hash
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

def create_diff(
    db,
    competitor_id: int,
    old_snapshot_id: int,
    new_snapshot_id: int,
    diff_text: str
):
    diff = DiffResult(
        competitor_id=competitor_id,
        old_snapshot_id=old_snapshot_id,
        new_snapshot_id=new_snapshot_id,
        diff_text=diff_text
    )
    db.add(diff)
    db.commit()
    db.refresh(diff)
def update_diff_summary(db, diff_id: int, summary: str):
    diff = db.query(models.DiffResult).filter(models.DiffResult.id == diff_id).first()
    if diff:
        diff.summary = summary
        db.commit()
    return diff
def get_last_diffs(db, competitor_id: int, limit: int = 5):
    return (
        db.query(DiffResult)
        .filter(DiffResult.competitor_id == competitor_id)
        .order_by(DiffResult.created_at.desc())
        .limit(limit)
        .all()
    )
   