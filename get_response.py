import requests
import json
import csv

def query_model(model, prompt):
    # OpenAI API key
    api_key = "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"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": prompt
            }
            ]
        }
        ],
        "max_tokens": 1000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    ans = response.json()['choices'][0]['message']['content']
    print(ans)
    print("---------------")

    return ans

def read_sentences_from_csv(file_path):
    """
    Reads sentences from a CSV file and returns them as a list.
    """
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

def generate_questions(sentence):
    Q1 = "Describe, step by step, how you would parse the sentence <" + sentence + ">, including identifying the main subject, verb, and any objects or complements."
    Q2 = "Read the following sentence and explain its meaning:" + sentence
    Q3 =  "Rephrase the sentence <" + sentence + "> to make its meaning clearer. Explain how your rephrasing helps to resolve any syntactic ambiguities."
    Q4 = "Why might the sentence <" + sentence + "> be confusing at first? Discuss both syntactic structure and potential semantic misinterpretations."
    
    return {"Parsing Methodology" : Q1, " Initial Interpretation" : Q2, "Rephrasing for Clarity" : Q3, "Analysis of Confusion" : Q4}

def main():

    # Models to query
    models = ["gpt-4", "gpt-4-1106-preview", "gpt-3.5-turbo-1106"]

    # Structure to hold the data
    data = {}

    # Read sentences from CSV file
    sentences = read_sentences_from_csv('Sentences/garden_path_sentences.csv')
    tot = len(sentences)

    for i in range(tot):
        print("Progress: Sentence " + str(i) + " out of " + str(tot))
        print("==================")
        sentence = sentences[i]
        data[sentence] = {}
        
        questions = generate_questions(sentence)  

        for type, question in questions.items():
            print("Working on: " + type)
            data[sentence][type] = {}
            for model in models:
                print("Working with model: " + str(model))
                response = query_model(model, question)
                data[sentence][type][model] = response
        print("==================")
    # Writing data to a JSON file
    with open("Data/sentence_responses.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
