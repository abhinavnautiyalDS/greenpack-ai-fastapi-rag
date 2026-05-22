import pandas as pd
from app.utils.percentage_calculator import calculate_percentage_difference
from app.utils.constants import THRESHOLD_PERCENT


class ReconciliationService:

    @staticmethod
    def reconcile(declaration):

        erp_data = pd.read_csv("app/data/erp_feed.csv")

        filtered = erp_data[
            (erp_data["producer_id"] == declaration.producer_id)
            &
            (erp_data["month"] == declaration.month)
        ]

        results = []

        categories = {
            "rigid_plastic": declaration.rigid_plastic,
            "flexible_plastic": declaration.flexible_plastic,
            "multilayer_plastic": declaration.multilayer_plastic
        }

        for category, declared_value in categories.items():

            actual_row = filtered[filtered["category"] == category]

            if actual_row.empty:
                continue

            actual_value = float(actual_row.iloc[0]["procured_kg"])

            percentage_diff = calculate_percentage_difference(
                declared_value,
                actual_value
            )

            status = "flagged" if percentage_diff > THRESHOLD_PERCENT else "matched"

            results.append({
                "category": category,
                "declared_kg": declared_value,
                "procured_kg": actual_value,
                "difference_percent": percentage_diff,
                "status": status
            })

        return results