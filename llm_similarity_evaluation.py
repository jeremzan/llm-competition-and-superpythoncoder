# llm_similarity_evaluation.py
from gpt4all import GPT4All

def evaluate_similarity(wolfram_answer, model_answer, model_name):

    judge_llm = GPT4All(model_name)
    prompt = f"""### Human:
Evaluate the similarity of the following two answers on a scale from 0 to 1.0, where 0 means completely different and 1.0 means exactly the same. Use a wide range of the scale and be precise. For example, for slightly similar answers, you might reply '0.3', for moderately similar answers '0.5', and for highly similar but not identical answers '0.8'. Here are the two answers: 1. {wolfram_answer} and 2. {model_answer}. Provide only the similarity score as a number without any additional text.
### Assistant:"""
        
    similarity_score = judge_llm.generate(prompt)

    return similarity_score




# """### Human:
# Rate the similarity of these two answers on a scale of 0-1.0. Provide your response as a single number, with no additional text. For example, if the answers are almost identical, reply '0.9'. If they are entirely different, reply '0.1'. Here are the two answers: 1. {wolfram_answer} and 2. {model_answer}.
# ### Assistant:"""