import pytest
import os
from common.llm_client import LLMClient


def test_llm_client_requires_key(monkeypatch):
    monkeypatch.delenv("CANDIDATE_API_KEY", raising=False)
    with pytest.raises(ValueError):
        LLMClient()
