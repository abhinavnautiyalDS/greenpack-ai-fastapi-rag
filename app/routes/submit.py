from fastapi import APIRouter
from app.models.schemas import SubmitRequest
from app.db.database import SessionLocal, engine
from app.db.models import Declaration
from app.db.database import Base
from app.utils.helpers import generate_record_id

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/submit")
def submit_declaration(payload: SubmitRequest):

    db = SessionLocal()

    declaration = Declaration(
        record_id=generate_record_id(),
        producer_id=payload.producer_id,
        month=payload.month,
        rigid_plastic=payload.declared_quantities_kg.get("rigid_plastic", 0),
        flexible_plastic=payload.declared_quantities_kg.get("flexible_plastic", 0),
        multilayer_plastic=payload.declared_quantities_kg.get("multilayer_plastic", 0)
    )

    db.add(declaration)
    db.commit()
    db.refresh(declaration)

    return {
        "message": "Declaration stored successfully",
        "record_id": declaration.record_id,
        "producer_id": declaration.producer_id,
        "month": declaration.month
    }