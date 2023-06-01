from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline

# Code from https://github.com/PromtEngineer/localGPT/blob/main/run_localGPT.py#L19
def load_vicuna_model():
    '''
    Select a model on huggingface. 
    If you are running this for the first time, it will download a model for you. 
    subsequent runs will use the model from the disk. 
    '''
    model_id = "TheBloke/vicuna-7B-1.1-HF"
    tokenizer = LlamaTokenizer.from_pretrained(model_id)

    model = LlamaForCausalLM.from_pretrained(model_id,
                                            #   load_in_8bit=True, # set these options if your GPU supports them!
                                            #   device_map=1#'auto',
                                            #   torch_dtype=torch.float16,
                                            #   low_cpu_mem_usage=True
                                              )

    pipe = pipeline(
        "text-generation",
        model=model, 
        tokenizer=tokenizer, 
        max_length=2048,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15
    )

    return HuggingFacePipeline(pipeline=pipe)