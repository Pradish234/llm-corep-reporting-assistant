# llm-corep-reporting-assistant

The project is a prototype for an **LLM-assisted regulatory reporting assistant** that assists UK banks in preparing PRA COREP returns.

The assistant zeroes in on a **constrained and well-scoped subset of COREP**, namely **COREP C 01.00 – Own Funds**.
Given:

a natural-language regulatory question, and

a basic reporting scenario

Relevant regulatory text is retrieved within the system, structured output is generated through an LLM, the output is mapped into a human-readable COREP template extract, basic validation rules are applied, and an audit log produced that links each populated field to the relevant regulatory source.

This prototype is meant to demonstrate **end-to-end behaviour**; it does not contain production-grade regulatory calculations.

One thing is:
Overview Architecture
Why an LLM-assisted approach?
COREP reporting involves the translation of dense regulatory guidance into forms by mapping them into structured reporting templates.
An LLM is very suitable for:

- interpreting regulatory text.
- generating schema-constrained structured outputs,
Supporting traceability and explainability.
Why a Local Open-Source LLM (Ollama)
This prototype avoids paid dependencies by using a **locally hosted open source LLM (Mistral)** via **Ollama**:
