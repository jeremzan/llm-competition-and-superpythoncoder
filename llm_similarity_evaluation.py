# llm_similarity_evaluation.py
from gpt4all import GPT4All

def evaluate_similarity(wolfram_answer, model_answer, model_name):

    judge_llm = GPT4All(model_name)
    prompt = f"""### Human:
Rate the similarity of these two answers on a scale of 0-1.0. Provide your response as a single number, with no additional text. For example, if the answers are almost identical, reply '0.9'. If they are entirely different, reply '0.1'. Here are the two answers: 1. {wolfram_answer} and 2. {model_answer}.
### Assistant:"""
        
    similarity_score = judge_llm.generate(prompt)

    return similarity_score



# # Example usage
# question = "What is the capital of France?"
# wolfram_answer = "Paris"
# model_answer = "Dakar"
# model_name = "mistral-7b-openorca.Q4_0.gguf"
# result = evaluate_similarity(wolfram_answer, model_answer, model_name)
# print(result)



# """### Human:
# Here are two answers to a question. Output on a scale of 0-1.0 how similar the two answers are. Here are the two answers: 1. {wolfram_answer} and 2. {model_answer}. Answer ONLY with a number between 0 and 1.0. NO ADDITIONAL TEXT. 
# Here are some examples of valid answers: 
# My prompt : Here are two answers to a question. Output on a scale of 0-1.0 how similar the two answers are. Here are the two answers: 1. boat and 2. ship. Answer only with a number between 0 and 1.0. 
# Your answer : 0.9.
# My prompt : Here are two answers to a question. Output on a scale of 0-1.0 how similar the two answers are. Here are the two answers: 1. cheetah and 2. chips. Answer only with a number between 0 and 1.0.
# Your answer : 0.1.
# ### Assistant:"""