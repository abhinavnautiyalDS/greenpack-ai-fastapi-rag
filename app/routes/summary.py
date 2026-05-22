from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import Declaration
from app.services.reconciliation import ReconciliationService
from app.services.llm_service import generate_completion

router = APIRouter()


@router.get("/summary/{producer_id}/{month}")
def get_summary(producer_id: str, month: str):

    db = SessionLocal()

    declaration = db.query(Declaration).filter(
        Declaration.producer_id == producer_id,
        Declaration.month == month
    ).first()

    if not declaration:
        return {
            "error": "Declaration not found"
        }

    reconciliation_result = ReconciliationService.reconcile(declaration)

    prompt = f"""
    Create a 3-5 sentence compliance summary based on this reconciliation result.

    {reconciliation_result}

    Mention mismatches and suggest corrective action.
    """

    narrative = generate_completion(prompt)

    return {
        "reconciliation": reconciliation_result,
        "narrative": narrative
    }