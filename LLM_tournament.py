import csv
import time
import requests
from gpt4all import GPT4All

# Replace with your Wolfram Alpha API key and the local LLM model name
WOLFRAM_ALPHA_API_KEY = 'your_wolfram_alpha_api_key'
LOCAL_LLM_MODEL = 'gpt4all-falcon-q4_0.gguf'

def query_wolfram_alpha(question):
    # Implement the API call to Wolfram Alpha
    url = f"http://api.wolframalpha.com/v2/query?input={question}&appid={WOLFRAM_ALPHA_API_KEY}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the response to get the answer
        # This is simplified; actual implementation depends on Wolfram's response structure
        data = response.json()
        answer = data['some_answer_field']
        return answer
    else:
        return None

def evaluate_similarity(question, wolfram_answer, model_answer):
    # Use a local LLM to evaluate similarity
    local_llm = GPT4All(LOCAL_LLM_MODEL)
    prompt = f"Here is a question: {question}. Do not try to solve the question. Here are two answers to that question. Output on a scale of 0-1.0 how similar the two answers are. Here are the two answers: 1. {wolfram_answer} and 2. {model_answer}"
    similarity_score = local_llm.query(prompt)
    return similarity_score

def query_model(model_name, question):
    model = GPT4All(model_name)
    output = model.generate("""### Human:
""" + question + """
### Assistant:""")
    return output

def main():
    results = []
    models = ["orca-2-7b.Q4_0.gguf", "mistral-7b-openorca.Q4_0.gguf"]  

    with open('questions.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            category, question = row
            wolfram_answer = query_wolfram_alpha(question)

            if wolfram_answer:
                for model in models:
                    start_time = time.time()
                    model_answer = query_model(model, question)
                    end_time = time.time()
                    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

                    similarity = evaluate_similarity(question, wolfram_answer, model_answer)

                    results.append({
                        "Question": question,
                        "Model": model,
                        "Answer": model_answer,
                        "TimeInMillisecondsToGetAnswer": int(time_taken),
                        "Correctness": similarity
                    })

    # Print or process the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()

