from yandex_cloud_ml_sdk import YCloudML
from shared.config import get_settings

from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_community.llms import YandexGPT
from langchain_core.prompts import PromptTemplate


class YandexGPTClient:
    def __init__(self):
        settings = get_settings()
        
        self.sdk = YCloudML(
            folder_id=settings.YA_GPT_FOLDER_ID,
            auth=settings.YANDEX_CLOUD_OAUTH_TOKEN
        )
        self._yandex_cloud_ml_model = self.sdk.models.completions("yandexgpt")
        self._yandex_gpt_model = YandexGPT(api_key=settings.YANDEX_CLOUD_SERVICE_ACCOUNT_API_KEY, folder_id=settings.YA_GPT_FOLDER_ID)
        
    def get_response(self, prompt: str):
        return self._yandex_cloud_ml_model.run(prompt)
    
    def get_chain_response(self, chained_prompts: list[str], enter_point: str) -> str | None:
        chains = []
        chain_results = []
        for generation_template in chained_prompts:
            prompt = PromptTemplate.from_template(generation_template)
            result = LLMChain(prompt=prompt, llm=self._yandex_gpt_model)
            chains.append(result)
            chain_results.append(result.invoke(enter_point))

        overall_simple_chain = SimpleSequentialChain(chains=chains, verbose=True)
        result = overall_simple_chain.invoke(enter_point)
        if "output" not in result:
            return None
        return result["output"]