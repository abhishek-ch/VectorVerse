from langchain.prompts import PromptTemplate
prompt_template = """Use the following pieces of context from vector database to answer the question at the end.
Summarize the key points from the context.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Before Final Answer, re verify your answer and if your answer is wrong, regenerate the answer.

{context}

Question: {question}
Answer:
Final Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)