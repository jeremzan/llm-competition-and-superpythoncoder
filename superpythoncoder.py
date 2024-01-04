import subprocess
import os
from openai import OpenAI
from dotenv import load_dotenv
import random
import re

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
    """Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

        Symbol       Value
        I             1
        V             5
        X             10
        L             50
        C             100
        D             500
        M             1000
        For example, 2 is written as II in Roman numeral, just two one's added together. 12 is written as XII, which is simply X + II. The number 27 is written as XXVII, which is XX + V + II.

        Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

        I can be placed before V (5) and X (10) to make 4 and 9. 
        X can be placed before L (50) and C (100) to make 40 and 90. 
        C can be placed before D (500) and M (1000) to make 400 and 900.
        Given an integer, convert it to a roman numeral.""",
]

    user_input = input("Tell me, which program would you like me to code for you? (press enter for a random program): ")

    if not user_input.strip():
        random_index = random.randint(0, len(PROGRAMS_LIST) - 1)
        user_input = PROGRAMS_LIST[random_index]

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

My prompt : "You are an expert python developer. Create for me : """ + user_input.strip() + """. Do not write any explanations, just show me the code itself. Also please include unit tests (using "assert =")that check the logic of the program using 5
different inputs and expected outputs. Print a sentence like "All tests passed" or "This test has failed...". Note that if you provided a answer that wasn't exclusively code, it might cause an error since the answer is not valid python code. IN ANY CASE, write ONLY python code, NO EXPLANATIONS NOR APOLOGIES.
If there was an error in the previous response that you provided, here's the error: """ + error_message + """. If there is nothing after the column just ignore the last sentence about the error. 
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

            # Use regular expression to find the line number and the error message
            error_match = re.search(r'line (\d+).*?Error:(.*)', error_message, re.DOTALL)
            
            if error_match:
                line_number = error_match.group(1)
                error_description = error_match.group(2).strip().split("\n")[0]  # Gets the first line of the error description
                error_message = f"Error at line {line_number}: {error_description}"

            print(f"Attempt {attempt + 1}: Error running generated code! Error: {error_message}")
    
    print("Code generation FAILED")  # Only reached if all attempts fail

if __name__ == "__main__":
    main()




# """Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer (similar to C/C++'s atoi function). The algorithm for myAtoi(string s) is as follows: Read in and ignore any leading whitespace. Check if the next character (if not already at the end of the string) is '-' or '+'. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored. Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2). If the integer is out of the 32-bit signed integer range [-231, 231 - 1], then clamp the integer so that it remains in the range. Specifically, integers less than -231 should be clamped to -231, and integers greater than 231 - 1 should be clamped to 231 - 1. Return the integer as the final result."""
    