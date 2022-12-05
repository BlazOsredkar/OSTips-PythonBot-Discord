import random
def handle_respone(message) -> str:
    p_message = message.lower()

    if p_message in greetings:
        return random.choice(greetings)
    if p_message == "Roll":
        return random.choice(rolls)