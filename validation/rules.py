from typing import Dict, List


class CorepValidator:
    """
    Basic validation rules for COREP C 01.00 (Own Funds).
    These rules are intentionally simple and transparent.
    """

    def validate(self, report: Dict) -> List[str]:
        validation_flags = []

        items = report.get("own_funds_items", [])

        values = {}
        for item in items:
            values[item["field_code"]] = item.get("amount")

            if item.get("amount") is None:
                validation_flags.append(
                    f"Missing value for field {item['field_code']} ({item['field_name']})"
                )

        cet1 = values.get("CET1_010")
        tier1 = values.get("T1_020")
        total = values.get("OF_030")

        if cet1 is not None and tier1 is not None:
            if tier1 < cet1:
                validation_flags.append(
                    "Tier 1 capital is lower than CET1 capital, which is inconsistent."
                )

        if tier1 is not None and total is not None:
            if total < tier1:
                validation_flags.append(
                    "Total own funds are lower than Tier 1 capital, which is inconsistent."
                )

        return validation_flags
