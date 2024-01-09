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
    ratings_sum = {model: 0 for model in models}
    lowest_rating = {model: (None, None, 1.0) for model in models}  # (question, answer, rating)
    questions_answered = 0

    with open('General_Knowledge_Questions.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            _, question = row
            wolfram_answer = query_wolfram_alpha(question, WOLFRAM_ALPHA_API_KEY)
            print()
            print(wolfram_answer)
            print()
            if wolfram_answer:
                
                for model in models:
                    start_time = time.time()
                    model_answer = query_model(model, question)
                    end_time = time.time()
                    time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
                    print("Got the " + model + " answer, checking for similarity with wolfram...")
                    print()
                    similarity = float(evaluate_similarity(wolfram_answer, model_answer, JUDGE_LLM_MODEL))
                    ratings_sum[model] += similarity

                    if similarity < lowest_rating[model][2]:  # Compare with the rating part of the tuple
                        lowest_rating[model] = (question, model_answer, similarity)  # Store question, answer, and rating

                    results.append({
                        "Question": question,
                        "Model": model,
                        "Answer": model_answer,
                        "TimeInMillisecondsToGetAnswer": float(time_taken),
                        "Correctness": similarity
                    })
                    print(f"Answer : {results[-1]['Answer']}, Correctness : {results[-1]['Correctness']}")
                    print()

                questions_answered += 1

            # # Limit to the first 5 rows for testing
            if questions_answered >= 5:
                break

    # Print or process the results
    # for result in results:
    #     print(result)

    # Print summary statistics
    print(f"\nNumber of questions answered: {questions_answered}")

    # First loop to print average ratings for all models
    for model in models:
        avg_rating = ratings_sum[model] / questions_answered if questions_answered > 0 else 0
        print(f"Average answer rating of {model}: {avg_rating:.2f}")
    
    # Second loop to print the lowest rated question and answer for all models
    for model in models:
        lowest_question, lowest_answer, lowest_rate = lowest_rating[model]
        if lowest_question:
            print(f"Lowest rating question and answer of {model}: {lowest_question} {lowest_answer}")

if __name__ == "__main__":
    start_time_ = time.time()
    main()
    end_time_ = time.time()
    
    hours, rem = divmod(end_time_ - start_time_, 3600)
    minutes, seconds = divmod(rem, 60)

    print("Total time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


    

    


