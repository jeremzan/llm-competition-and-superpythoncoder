# wolfram_alpha_query.py
import requests
import redis
from urllib.parse import quote_plus


# Initialize the Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def query_wolfram_alpha(question, api_key):

    # Check if the answer is already in Redis cache
    cached_answer = redis_client.get(question)
    if cached_answer:
        print("cached")
        return cached_answer

    # If not in cache, call Wolfram Alpha API
    formatted_question = quote_plus(question)

    url = f"http://api.wolframalpha.com/v1/result?input={formatted_question}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        answer = response.text
        # Cache the answer in Redis with a 4-hour expiration
        redis_client.setex(question, 14400, answer)  # 14400 seconds = 4 hours
        return answer
    
    else:
        return None

