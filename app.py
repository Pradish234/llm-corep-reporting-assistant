import json

from retrieval.rag import RegulatoryRAG
from llm.generator import LLMGenerator
from validation.rules import CorepValidator
from validation.template_mapper import CorepTemplateMapper
from audit.audit_log import AuditLogger

from langchain_core.embeddings import Embeddings



def load_schema(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class DummyEmbeddings(Embeddings):
    """
    Deterministic dummy embeddings for prototype purposes.
    Avoids paid APIs while enabling vector search.
    """

    def embed_documents(self, texts):
        return [[float(len(text))] * 10 for text in texts]

    def embed_query(self, text):
        return [float(len(text))] * 10

def main():
    print("LLM-Assisted PRA COREP Reporting Assistant (Prototype)")
    print("-" * 55)

    # -----------------------------
    # User input (simplified)
    # -----------------------------
    # -----------------------------
# User input (interactive)
# -----------------------------
    print("\nEnter your regulatory reporting question:")
    question = input("> ").strip()

    print("\nEnter a brief reporting scenario:")
    scenario = input("> ").strip()

    

    # -----------------------------
    # Load schema
    # -----------------------------
    schema = load_schema("schemas/corep_c01_schema.json")

    # -----------------------------
    # Retrieval setup
    # -----------------------------
    embedding_model = DummyEmbeddings()


    rag = RegulatoryRAG(
        documents_path=[
            "data/pra_rulebook/own_funds.md",
            "data/corep_instructions/corep_c01.md",
        ],
        embedding_model=embedding_model,
    )

    retrieved_docs = rag.retrieve(question)

    # -----------------------------
    # LLM-assisted generation (mock)
    # -----------------------------
    generator = LLMGenerator()
    structured_report = generator.generate(
        question=question,
        scenario=scenario,
        retrieved_docs=retrieved_docs,
        schema=schema,
    )

    # -----------------------------
    # Validation
    # -----------------------------
    validator = CorepValidator()
    validation_flags = validator.validate(structured_report)
    structured_report["validation_flags"] = validation_flags

    # -----------------------------
    # Template mapping
    # -----------------------------
    mapper = CorepTemplateMapper()
    template_table = mapper.map_to_table(structured_report)

    # -----------------------------
    # Audit log
    # -----------------------------
    audit_logger = AuditLogger()
    audit_log = audit_logger.build_audit_log(structured_report)

    # -----------------------------
    # Output results
    # -----------------------------
    print("\nCOREP C 01.00 – Own Funds (Extract)")
    print("-" * 40)
    for row in template_table:
        print(row)

    print("\nValidation Flags")
    print("-" * 40)
    if validation_flags:
        for flag in validation_flags:
            print(f"- {flag}")
    else:
        print("No validation issues detected.")

    print("\nAudit Log")
    print("-" * 40)
    for entry in audit_log:
        print(entry)


if __name__ == "__main__":
    main()
