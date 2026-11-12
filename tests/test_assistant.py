"""Retrieval finds the right passage, prompts stay grounded, the knowledge base is current
and contains nothing private."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_knowledge  # noqa: E402
from retrieval import BM25Index, tokenize  # noqa: E402

st = pytest.importorskip("streamlit")
import app  # noqa: E402


@pytest.fixture(scope="module")
def index() -> BM25Index:
    return BM25Index.from_file()


def test_snake_case_identifiers_are_split():
    assert tokenize("fct_account_monthly") == ["fct_account_monthly", "fct", "account", "monthly"]


@pytest.mark.parametrize(
    ("question", "expected_in_top3"),
    [
        ("What does Karthikeyan do at Autodesk?", "autodesk"),
        ("What did Karthikeyan do at ExxonMobil?", "exxonmobil"),
        ("What is Scout and how was it built?", "copilot studio"),
        ("How does Karthikeyan make sure the numbers are right?", "refresh"),
        ("Tell me about the churn model", "leakage"),
        ("Where did Karthikeyan study?", "christ university"),
        ("What certificates does Karthikeyan have?", "snowflake"),
        ("What was the hardest problem in the bank data platform?", "ledger"),
        ("Why both Airflow and Dagster?", "dagster"),
        ("What projects are in the portfolio?", "bank data platform"),
        ("How can I contact Karthikeyan?", "linkedin"),
    ],
)
def test_questions_retrieve_the_relevant_passage(index, question, expected_in_top3):
    top = index.search(question, k=3)
    blob = " ".join(f"{h.chunk['title']} {h.chunk['text']}" for h in top).lower()
    assert expected_in_top3 in blob


def test_unrelated_question_finds_little(index):
    assert len(index.search("zzqx flibbertigibbet", k=3)) == 0


def test_prompt_carries_rules_context_and_trimmed_history(index):
    hits = index.search("Scout", k=2)
    history = [{"role": "user", "content": f"q{i}"} for i in range(20)]
    msgs = app.build_messages("What is Scout?", hits, history)
    system = msgs[0]["content"]
    assert msgs[0]["role"] == "system" and "Answer only from the CONTEXT" in system
    assert "gendered pronouns" in system and "salary" in system
    assert "CONTEXT:" in msgs[-1]["content"] and "What is Scout?" in msgs[-1]["content"]
    assert len(msgs) == 1 + 2 * app.MAX_HISTORY_TURNS + 1


def test_retrieval_only_answer_works_without_a_token(index):
    text = app.retrieval_only_answer(index.search("bank data platform quality gate", k=3))
    assert "HF_TOKEN" in text and "[" in text
    assert "couldn't find" in app.retrieval_only_answer([])


def test_every_chunk_links_to_a_public_source(index):
    for c in index.chunks:
        assert c["source"] and c["url"].startswith("https://github.com/Karthikeyan314/")


def test_knowledge_base_has_no_private_data(index):
    assert build_knowledge.privacy_violations(index.chunks) == []


@pytest.mark.parametrize(
    "text",
    ["call +91 98765 43210", "mail someone@example.com", "Confidential draft", "SCRATCH_BOOK"],
)
def test_privacy_check_catches_private_looking_text(text):
    chunk = {"title": "t", "source": "s", "text": text}
    assert build_knowledge.privacy_violations([chunk])


def test_knowledge_base_is_up_to_date():
    """CI fails if the profile or snapshots changed but chunks.jsonl was not rebuilt."""
    kb = ROOT / "knowledge" / "chunks.jsonl"
    before = kb.read_text(encoding="utf-8")
    subprocess.run(
        [sys.executable, str(ROOT / "build_knowledge.py")], check=True, capture_output=True
    )
    after = kb.read_text(encoding="utf-8")
    assert before == after, "run: python build_knowledge.py"
    assert all(json.loads(line)["source"] for line in after.splitlines())
