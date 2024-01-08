# main_program.py
import csv
import time
from dotenv import load_dotenv
import os
from wolfram_alpha_query import query_wolfram_alpha
from llm_similarity_evaluation import evaluate_similarity
from model_query import query_model

load_dotenv()

WOLFRAM_ALPHA_API_KEY = os.environ.get("WOLFRAM_ALPHA_API_KEY")
JUDGE_LLM_MODEL = 'mistral-7b-openorca.Q4_0.gguf'

def main():
    results = []
    models = ["orca-2-7b.Q4_0.gguf", "mistral-7b-openorca.Q4_0.gguf"]  
    
    with open('questions.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            _, question = row
            wolfram_answer = query_wolfram_alpha(question, WOLFRAM_ALPHA_API_KEY)

            if wolfram_answer:
                for model in models:
                    start_time = time.time()
                    model_answer = query_model(model, question)
                    end_time = time.time()
                    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

                    similarity = evaluate_similarity(question, wolfram_answer, model_answer, JUDGE_LLM_MODEL)

                    results.append({
                        "Question": question,
                        "Model": model,
                        "Answer": model_answer,
                        "TimeInMillisecondsToGetAnswer": float(time_taken),
                        "Correctness": similarity
                    })

    # Print or process the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
