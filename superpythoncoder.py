import subprocess
import os
from openai import OpenAI
from dotenv import load_dotenv
import random

def main():

    load_dotenv()

    client = OpenAI(api_key=os.environ.get("HW1_PYTHONKEY"))

    # List of program ideas
    PROGRAMS_LIST = [
    """Given two strings str1 and str2, prints all interleavings of the given two strings. 
       You may assume that all characters in both strings are different.
       Input: str1 = "AB",  str2 = "CD"
       Output: ABCD ACBD ACDB CABD CADB CDAB
       Input: str1 = "AB",  str2 = "C"
       Output: ABC ACB CAB""",
    "a program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree.",
    "A program that finds the median number of a binary search tree.",
]

    user_input = input("Tell me, which program would you like me to code for you? (press enter for a random program): ")

    if not user_input.strip():
        user_input = random.choice(PROGRAMS_LIST)

    error_message = ""

    for attempt in range(5):
        prompt = """My prompt :"You are an expert javascript developer. Create for me a javascript program that prints whatever the user is writing in the input. Do not write any explanations, just show me the code itself."
Your answer:
// Import the readline module
const readline = require('readline');

// Create an interface for input and output
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Prompt the user for input
rl.question('Please enter some input: ', (input) => {
  // Print the user's input
  console.log(`You entered: ${input}`);

  // Close the readline interface
  rl.close();
});

My prompt : "You are an expert python developer. Create for me : """ + user_input.strip() + """. Do not write any explanations, just show me the code itself. Also please include unit tests that check the logic of the program using 5
different inputs and expected outputs. Print a sentence like "All tests passed" or "This test has failed...". Here is the error that I got when you provided an answer: """ + error_message + """. If this is empty then don't worry about it.
Your answer : """
        # Generate code using OpenAI API
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        ai_response = completion.choices[0].message.content

        # Write the generated code to a file
        with open('generatedcode2.py', 'w') as file:
            file.write(ai_response)

        # Try running the generated code
        try:
            subprocess.run(["python3", "generatedcode2.py"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Code creation completed successfully!")
            subprocess.call(["open", "generatedcode2.py"])
            return # Exit the loop after successful execution
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode()
            print(f"Attempt {attempt + 1}: Error running generated code! Error: {error_message}")
    
    print("Code generation FAILED")  # Only reached if all attempts fail

if __name__ == "__main__":
    main()
