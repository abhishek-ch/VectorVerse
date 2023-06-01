from enum import Enum

# Define your Enum class
class Model(Enum):
    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4-0314"
    GPT4ALL = "GPT4All"
    LLAMA = "LlamaCpp"
    VICUNA_7B = "Vicuna-7B"

models = [Model.GPT3_5.value,  Model.GPT4ALL.value, Model.GPT4.value, Model.LLAMA.value, Model.VICUNA_7B.value]