from gpt4all import GPT4All

model = GPT4All("orca-2-7b.Q4_0.gguf")
output = model.generate("Answer this prompt by saying 'Hello LLM'")
print(output)