# model_query.py
from gpt4all import GPT4All

def query_model(model_name, question):
    model = GPT4All(model_name)
    output = model.generate("""### Human:
""" + question + """
### Assistant:""")
    return output


# # Example usage
# question = "What is the capital of France?"
# model_name = "mistral-7b-openorca.Q4_0.gguf"
# result = query_model(model_name, question)
# print(result)




