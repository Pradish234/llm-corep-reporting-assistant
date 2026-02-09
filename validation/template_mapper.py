from typing import Dict, List


class CorepTemplateMapper:
    """
    Maps structured COREP output into a human-readable COREP template extract.
    Ensures clean and regulator-safe rule reference formatting.
    """

    def map_to_table(self, report: Dict) -> List[Dict]:
        table = []

        for item in report.get("own_funds_items", []):
            source_rule = item.get("source_rule", {})

            section = source_rule.get("section", "").strip()
            paragraph = source_rule.get("paragraph", "").strip()

            # Clean, deterministic rule reference formatting
            if section and paragraph:
                rule_reference = f"{section} para {paragraph}"
            elif paragraph:
                rule_reference = f"para {paragraph}"
            else:
                rule_reference = "Not specified"

            table.append(
                {
                    "Field Code": item["field_code"],
                    "Description": item["field_name"],
                    "Amount (GBP)": item["amount"],
                    "Rule Reference": rule_reference,
                }
            )

        return table
