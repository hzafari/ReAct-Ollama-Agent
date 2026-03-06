from llm import LocalLLM
from agent import ReActAgent

if __name__ == "__main__":
    llm = LocalLLM(model="llama3")  # change if needed
    agent = ReActAgent(llm)



    # question = input("Ask: ")
    # result = agent.run(question)

    # print("\nFINAL ANSWER:\n", result)

    print("Agent ready. Type 'exit' to quit.\n")

    while True:
        question = input("Ask: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("Exiting agent. Bye!")
            break

        result = agent.run(question)
        print("\nFINAL ANSWER:\n", result)
        print("\n" + "="*50 + "\n")