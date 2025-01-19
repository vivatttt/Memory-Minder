import asyncio
from frontend.bot.games.n_back import NBackGame

class UserSession:
    def __init__(self):
        self.choice_event = asyncio.Event()
        self.choice_values = []
        self.right_values = []

def with_game_slug(st: str) -> str:
    return f"{NBackGame.slug}_{st}"

def output_results(user):
    res = "Ответы:  Ваш  Верный"
    for choice, right in zip(user.choice_values, user.right_values):
        if choice == right:
            res += "\n    ✅{:>12} {:>11}".format(choice, right)
        else:
            res += "\n    ❌{:>12} {:>11}".format(choice, right)
    return res

def generate_examples(user, n=1):
    import random
    examples = []
    for i in range(n):
        sign = random.choice(["+", "-"])
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        if n != 1:
            examples.append(f"{i+1}) {a} {sign} {b}")
        else:
            examples.append(f"{a} {sign} {b}")
        if sign == "+": 
            user.right_values.append(str(a+b)[-1]) 
        else:
            user.right_values.append(str(a-b)[-1]) 
    return "\n".join(examples)
    