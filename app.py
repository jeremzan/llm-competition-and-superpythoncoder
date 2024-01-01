import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess


load_dotenv()

client = OpenAI(api_key=os.environ.get("HW1_PYTHONKEY"),)

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content" : """My prompt :"You are an expert javascript developer. Create for me a javascript program that prints whatever the user is writing in the input. Do not write any explanations, just show me the code itself."
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

My prompt : "You are an expert python developer. Create for me a python program that checks if the input that 25is a number is prime. Do not write any explanations, just show me the code itself. Also please include unit tests that check the logic of the program using 5
different inputs and expected outputs. Print a sentence like "All tests passed" or "This test has failed..."."
Your answer : """,
        }
    ],
    model="gpt-3.5-turbo",
)


# Getting the AI's response
ai_response = completion.choices[0].message.content

# Writing the response to a file
with open('generatedcode.py', 'w') as file:
    file.write(ai_response)

# Run the generatedcode.py file
subprocess.run(["python3", "generatedcode.py"])
