from typing import Dict, List


class AuditLogger:
    """
    Constructs a clean, deterministic audit log.
    Normalizes rule references to avoid LLM formatting issues.
    """

    def build_audit_log(self, report: Dict) -> List[Dict]:
        audit_entries = []

        for item in report.get("own_funds_items", []):
            source = item.get("source_rule", {})

            section = source.get("section", "").strip()
            paragraph = source.get("paragraph", "").strip()

            # Normalize section and paragraph
            section = section.replace("Section", "").strip()
            paragraph = paragraph.replace("para", "").strip()

            audit_entries.append(
                {
                    "field_code": item.get("field_code"),
                    "field_name": item.get("field_name"),
                    "amount": item.get("amount"),
                    "rulebook": source.get("rulebook", "PRA Rulebook"),
                    "section": section,
                    "paragraph": paragraph,
                }
            )

        return audit_entries
