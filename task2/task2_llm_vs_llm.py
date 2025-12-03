from common.llm_client import LLMClient
from common.game_models import GameState, parse_llm_guess
from common.players import (
    llm_choose_secret_object,
    llm_answer_question,
    llm_generate_question,
    llm_generate_final_guess,
)


def play_llm_vs_llm():
    print("\n=== Task 2 — LLM vs LLM ===\n")

    llm = LLMClient()
    state = GameState()

    # This now uses the diversified chooser from common.players:
    # LLM proposes a list of objects; we randomly pick one.
    state.secret_object = llm_choose_secret_object(llm)
    print(f"[DEBUG] Player 1's secret object: {state.secret_object}\n")

    while not state.finished:
        remaining = state.max_questions - state.num_questions_asked

        if remaining <= 0:
            print(
                "\nThe LLM questioner ran out of moves without making a guess. "
                "Player 1 (answerer) wins!"
            )
            state.winner = "player1"
            state.finished = True
            break

        # If this is the last move, force a final guess
        if remaining == 1:
            print("\n[DEBUG] LLM Questioner must now make a FINAL GUESS.")
            for attempt in range(3):
                try:
                    llm_output = llm_generate_final_guess(llm, state)
                except RuntimeError:
                    print(
                        "[DEBUG] LLM Questioner had trouble generating a final guess. Retrying..."
                    )
                    continue

                guess = parse_llm_guess(llm_output)
                if guess:
                    print(f"LLM Questioner FINAL GUESS: '{guess}'")
                    if guess.lower() == (state.secret_object or "").lower():
                        print("\nCorrect! Player 2 (questioner) wins!\n")
                        state.winner = "player2"
                    else:
                        print(
                            f"\nIncorrect. The secret object was '{state.secret_object}'. "
                            "Player 1 (answerer) wins!\n"
                        )
                        state.winner = "player1"
                    state.finished = True
                    break

            if not state.finished:
                print(
                    "\nThe LLM Questioner failed to make a valid guess. "
                    "Player 1 (answerer) wins by default!"
                )
                state.winner = "player1"
                state.finished = True

            break  # end loop regardless

        # Normal question phase (remaining > 1)
        try:
            llm_output = llm_generate_question(llm, state)
        except RuntimeError:
            print(
                "\n[DEBUG] LLM Questioner had trouble generating a question. "
                "Trying again...\n"
            )
            continue

        try:
            answer = llm_answer_question(llm, state.secret_object, llm_output)
        except RuntimeError:
            print(
                "\n[DEBUG] LLM Answerer had trouble answering. "
                "Treating answer as 'NO'.\n"
            )
            answer = "no"

        state.num_questions_asked += 1
        state.history.append((llm_output, answer))

        print(f"Q{state.num_questions_asked}: {llm_output}")
        print(f"Answerer replies: {answer.upper()}\n")

    print("Game over.\n")


if __name__ == "__main__":
    play_llm_vs_llm()
