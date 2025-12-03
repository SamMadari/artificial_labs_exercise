import re

from common.llm_client import LLMClient
from common.game_models import GameState, parse_yes_no, parse_llm_guess
from common.players import (
    llm_choose_secret_object,
    llm_answer_question,
    llm_generate_question,
    llm_generate_final_guess,
)
from common.players import _normalize_object  # reuse same normalization


def _extract_direct_guess_from_question(question: str) -> str | None:
    """
    Detect when the human is effectively making a direct guess via a question, e.g.:

        "Is it an apple?"
        "Is it a cat?"

    We require an article (a/an/the) and we return the guessed phrase if present.
    """
    q = question.strip()
    m = re.search(r"\bis it\s+(?:an?|the)\s+(.+?)[\?\.\!]*$", q, flags=re.I)
    if not m:
        return None
    guess_raw = m.group(1).strip()
    return guess_raw or None


def human_as_questioner():
    """
    Human is Player 2 (questioner), LLM is Player 1 (answerer).

    Enhancement: if the human asks a 'direct guess' question like
    'Is it an apple?' and that matches the secret object, we treat it
    as a winning guess and end the game immediately.
    """
    print("\n=== Task 1 — Mode A: You ask questions, LLM thinks of the object ===\n")

    llm = LLMClient()
    state = GameState()

    state.secret_object = llm_choose_secret_object(llm)
    print("The LLM has chosen a secret object.")
    print("You may ask up to 20 yes/no questions.")
    print("When you want to guess, you can either:")
    print("  - Type: guess: <your_guess>")
    print("  - Or ask a direct question like: 'Is it an apple?'\n")

    while not state.finished:
        if state.num_questions_asked >= state.max_questions:
            print("\nYou've used all your questions. You lose!")
            print(f"The secret object was: {state.secret_object}")
            state.finished = True
            break

        user_input = input(
            f"Question {state.num_questions_asked + 1} (or 'guess: <object>'): "
        ).strip()

        # Explicit guess via "guess: X"
        if user_input.lower().startswith("guess:"):
            guess = user_input.split(":", 1)[1].strip()
            if guess.lower() == (state.secret_object or "").lower():
                print("\nCorrect! You guessed the object. You win!\n")
                state.winner = "human"
            else:
                print(
                    f"\nIncorrect. The secret object was '{state.secret_object}'.\n"
                )
                state.winner = "llm"
            state.finished = True
            break

        # Implicit guess via question "Is it a/an/the X?"
        direct_guess = _extract_direct_guess_from_question(user_input)
        if direct_guess:
            guess_norm = _normalize_object(direct_guess)
            secret_norm = _normalize_object(state.secret_object or "")

            if guess_norm and guess_norm == secret_norm:
                print(
                    f"\nYour question was a direct guess ('{direct_guess}') "
                    "and it was RIGHT. You win!\n"
                )
                state.winner = "human"
                state.finished = True
                break
            else:
                print(
                    f"\nYour question was a direct guess ('{direct_guess}') "
                    f"and it was wrong. The object was '{state.secret_object}'.\n"
                )
                state.winner = "llm"
                state.finished = True
                break

        # Otherwise treat it as a normal yes/no question to the LLM
        try:
            answer = llm_answer_question(llm, state.secret_object, user_input)
        except RuntimeError:
            print(
                "\nThe AI had trouble answering that question. "
                "Please ask a simpler yes/no question.\n"
            )
            continue

        state.num_questions_asked += 1
        state.history.append((user_input, answer))

        print(f"LLM answers: {answer.upper()}\n")


def human_as_answerer():
    """
    Human is Player 1 (answerer), LLM is Player 2 (questioner).
    The orchestrator guarantees that the final move is always a GUESS, not a question.
    """
    print("\n=== Task 1 — Mode B: LLM asks questions, you think of the object ===\n")

    llm = LLMClient()
    secret = input(
        "Think of a secret object (e.g., 'cat', 'banana').\n"
        "Optionally type it here for evaluation, or press Enter to keep it private: "
    ).strip()
    if not secret:
        secret = None

    state = GameState(secret_object=secret)
    print("\nThe LLM will now try to guess your object by asking yes/no questions.")
    print("Please answer with 'yes' or 'no'.\n")

    while not state.finished:
        remaining = state.max_questions - state.num_questions_asked

        if remaining <= 0:
            print("\nThe LLM ran out of moves without guessing. You win!")
            state.winner = "human"
            state.finished = True
            break

        # If this is the last allowed move, force a final guess
        if remaining == 1:
            print("\nThe LLM must now make a FINAL GUESS.")
            for attempt in range(3):
                try:
                    llm_output = llm_generate_final_guess(llm, state)
                except RuntimeError:
                    print(
                        "The AI had trouble generating a final guess. Retrying..."
                    )
                    continue

                guess = parse_llm_guess(llm_output)
                if guess:
                    print(f"\nThe LLM makes a final guess: '{guess}'")
                    confirmation = input("Is this correct? (yes/no): ").strip()
                    yn = parse_yes_no(confirmation)
                    if yn == "yes":
                        print("\nThe LLM guessed correctly. It wins!\n")
                        state.winner = "llm"
                    else:
                        print("\nThe LLM guessed incorrectly. You win!\n")
                        state.winner = "human"
                    state.finished = True
                    break

            if not state.finished:
                print(
                    "\nThe LLM failed to make a valid guess after several attempts. You win!"
                )
                state.winner = "human"
                state.finished = True

            break  # end game loop regardless

        # Normal question phase (remaining > 1)
        try:
            llm_output = llm_generate_question(llm, state)
        except RuntimeError:
            print(
                "\nThe AI had trouble generating a question. "
                "We'll try again.\n"
            )
            continue

        print(f"\nLLM Question {state.num_questions_asked + 1}: {llm_output}")
        while True:
            human_answer = input("Your answer (yes/no): ").strip()
            yn = parse_yes_no(human_answer)
            if yn is None:
                print("Please answer with 'yes' or 'no'.")
                continue
            break

        state.history.append((llm_output, yn))
        state.num_questions_asked += 1

    print("Game over.\n")


def main():
    print("\n=== Task 1 — Human vs LLM ===\n")
    print("Choose your role:")
    print("1) You are the questioner (Player 2) — you guess the LLM's object.")
    print("2) You are the answerer (Player 1) — LLM tries to guess your object.\n")

    choice = input("Enter choice number: ").strip()
    if choice == "1":
        human_as_questioner()
    elif choice == "2":
        human_as_answerer()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
