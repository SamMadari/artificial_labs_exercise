from common.players import llm_answer_question


class MockLLM:
    def __init__(self, response):
        self.response = response

    def ask(self, *_args, **_kwargs):
        return self.response


def test_llm_answer_question_yes():
    llm = MockLLM("yes")
    assert llm_answer_question(llm, "cat", "Is it alive?") == "yes"


def test_llm_answer_question_no():
    llm = MockLLM("no")
    assert llm_answer_question(llm, "cat", "Is it a fruit?") == "no"
