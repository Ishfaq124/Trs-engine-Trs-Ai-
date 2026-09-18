import json
from .engine import Aurelith


def main():
    agent = Aurelith()

    print("Aurelith / TRS v2")
    print("Commands: /state, /self, /quit")

    while True:
        try:
            text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not text:
            continue
        if text == "/quit":
            break
        if text == "/state":
            print(json.dumps(agent.state(), indent=2))
            continue
        if text == "/self":
            print(agent.self_model.summary())
            continue

        print("\nAurelith:", agent.chat(text))


if __name__ == "__main__":
    main()
