from task1.task1_human_vs_llm import human_as_questioner, human_as_answerer
from task2.task2_llm_vs_llm import play_llm_vs_llm


def main():
    print("\n===================================================")
    print(" TWENTY QUESTIONS FOR ARTIICIAL LABS          ")
    print("===================================================\n")

    while True:
        print("Choose a mode:\n")
        print("1) Human vs LLM — you ask questions (Human = Player 2).")
        print("2) Human vs LLM — LLM asks, you answer (Human = Player 1).")
        print("3) LLM vs LLM.")
        print("4) Quit.\n")

        choice = input("Enter choice number: ").strip()

        if choice == "1":
            human_as_questioner()
        elif choice == "2":
            human_as_answerer()
        elif choice == "3":
            play_llm_vs_llm()
        elif choice == "4":
            print("\nGoodbye!\n")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
