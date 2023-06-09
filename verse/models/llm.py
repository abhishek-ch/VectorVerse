from langchain import OpenAI
from pydantic import BaseModel
from typing import List
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import os
from langchain.llms import GPT4All, LlamaCpp
from langchain.llms.base import BaseLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from verse.models.helper import *
from verse.models.vicuna import *

gpt_models_dict = {"gpt-3.5-turbo": "gpt-35-turbo", "gpt-4-0314": "gpt-4_8k_ascent"}


def get_model(model_name: str) -> BaseLLM:
    callbacks = [StreamingStdOutCallbackHandler()]
    match model_name:
        case Model.GPT3_5.value:
            return AzureChatOpenAI(
                deployment_name=gpt_models_dict.get(model_name), temperature=0.7
            )
        case Model.GPT4.value:
            return AzureChatOpenAI(
                deployment_name=gpt_models_dict.get(model_name), temperature=0.65
            )
        case "openai":
            return OpenAI(temperature=0.7)
        case Model.LLAMA.value:
            return LlamaCpp(
                model_path=os.environ.get("DOCKER_LLAMA_EMBEDDINGS_MODEL",os.environ["LLAMA_EMBEDDINGS_MODEL"]),
                temperature=0.6,
                n_ctx=2000,
            )
        case Model.GPT4ALL.value:
            return GPT4All(
                model=os.environ.get("DOCKER_MODEL_PATH",os.environ["MODEL_PATH"]),
                n_ctx=8000,
                backend="gptj",
                verbose=False,
                callbacks=callbacks,
                n_batch=10,
            )
        case Model.VICUNA_7B.value:
            return load_vicuna_model()
        case _default:
            print(f"Model {model_name} is not supported")
            exit


# class ChatLLM(BaseModel):
#     llm: BaseLLM = None

#     def __init__(self, model: str, **kwargs):
#         super().__init__(**kwargs)
#         self.llm = get_model(model)

#     def generate(self, prompt: str, stop: List[str] = None) -> BaseLLM:
#         if os.environ["MODEL_TYPE"].lower() in ["azure", "openai"]:
#             return self.llm([HumanMessage(content=prompt)], stop=stop)

#         RetrievalQA.from_chain_type(
#             llm=self.llm,
#             chain_type="stuff",
#             retriever=retriever,
#             return_source_documents=True,
#         )
