from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
import os


class GameLogic:
    def __init__(self):
        self.gigachat_key = os.environ["GIGACHAT_API_KEY"]
        self.llm = GigaChat(
            credentials=self.gigachat_key,
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            verify_ssl_certs=False,
            streaming=False,
        )
        self.words_num = 20

    def return_words(self, theme: str):
        messages = [SystemMessage(
            content=f"Ты бот, который возвращает в ответ на запрос пользователя ровно {self.words_num} случайных слов,"
                    f" подходящих под тематику запроса"), HumanMessage(content=theme)]
        result = self.llm.invoke(messages)
        return result.content

    def calculate_results(self, ai_text: str, user_text: str):
        ai_words = ai_text.lower().split(sep=', ')
        user_words = user_text.lower().split()
        right_guesses = 0
        for ai_word in ai_words:
            for user_word in user_words:
                if ai_word == user_word:
                    right_guesses += 1
        return (right_guesses, len(ai_words))
