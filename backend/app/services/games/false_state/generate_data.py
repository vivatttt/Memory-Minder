import re
from typing import Any

from backend.app.services.llm_clients import YandexGPTClient

y_gpt_client = YandexGPTClient()

class YandexGPTStupidResponseError(Exception):
    pass

class GenerateData:
    def __init__(self):
        self.ya_gpt = YandexGPTClient()

    def _parse_states(self, states: str, num_wrong_states: int, num_correct_states) -> dict[str]:
        states = states.replace("\n", " ")
        pattern = r"\[(.*?)\].*?\[(.*?)\]"

        try:
            matches = re.search(pattern, states, re.DOTALL)
            correct_states = [st for st in matches.group(1).split(";") if st]
            wrong_states = [st for st in matches.group(2).split(";") if st]
            # if num_wrong_states != len(wrong_states) or num_correct_states != len(correct_states):
            #     raise YandexGPTStupidResponse

        except Exception:
            wrong_states = []
            correct_states = []

        return {
            "wrong": wrong_states,
            "correct": correct_states,
        }

    def _get_states(self, prompt: str, wrong_states, correct_states):
        response = self.ya_gpt.get_response(
            prompt=prompt
        )
        return self._parse_states(response.alternatives[0].text, wrong_states, correct_states)

    def _get_text(self, prompts: list[str], enter_point: Any) -> str | None:
        return self.ya_gpt.get_chain_response(
            chained_prompts=prompts,
            enter_point=enter_point
        )

    def get_game_data(self, difficulty: int, wrong_states: int = 4, correct_states: int = 8):
        text = self._get_text(
            prompts=[
                ("Придумай тематику для текста, сложность которой для прочтения будет {difficulty}/10. В ответ напиши только название темы"), # noqa: E501
                ("Сгенерируй текст на 250 слов на тему {topic}.")
            ],
            enter_point=difficulty
        )
        states = self._get_states(
            prompt=f"""
            {text}
            Выдели ровно {correct_states} правильных утверждений из текста ниже
            и ровно {wrong_states} неправильных утверждений из текста ниже
            Не используй Markdown
            Ответ представь в виде
            правильные утверждения, разделенные ; в квадратных скобках
            с новой строки неправильные утверждения, разделенные ; в квадратных скобках
            """,
            wrong_states=wrong_states,
            correct_states=correct_states
        )
        return {
            "text": text,
            "statements": states
        }
