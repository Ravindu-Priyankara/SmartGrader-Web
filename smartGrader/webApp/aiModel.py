
import json
import random
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def load_json_file(filename):
    with open(filename) as f:
        file = json.load(f)
    return file

def create_df():
    df = pd.DataFrame({
        'Pattern' : [],
        'Tag' : []
    })
    
    return df

def extract_json_info(json_file, df):
    
    for intent in json_file['intents']:
        
        for pattern in intent['patterns']:
            
            sentence_tag = [pattern, intent['tag']]
            df.loc[len(df.index)] = sentence_tag
                
    return df

def collector(value):
    with open("data.log", 'a') as file:
        file.write(value[0])


def ai_model(data):
    filename = '/Users/ravindupriyankara/Career/SmartGrader-Web/smartGrader/webApp/dataset.json'

    intents = load_json_file(filename)

    df = create_df()
    df = extract_json_info(intents, df)
    df2 = df.copy()
    labels = df2['Tag'].unique().tolist()
    labels = [s.strip() for s in labels]
    num_labels = len(labels)
    id2label = {id:label for id, label in enumerate(labels)}
    label2id = {label:id for id, label in enumerate(labels)}



    model_path = "/Users/ravindupriyankara/Career/SmartGrader-Web/smartGrader/webApp/smg_model"
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizerFast.from_pretrained(model_path)
    smg = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    
    text = data.strip().lower()
    
    score = smg(text)[0]['score']
        
        
    label = label2id[smg(text)[0]['label']]

    all_responses = []
    
    for i in range(0, 10):
        all_responses.append(intents['intents'][label]['responses'][i])

    '''
     # Retrieve context_set for the given label
    label_context_sets = []
    for intent in intents['intents']:
        if 'tag' in intent and intent['tag'] == id2label[label]:
            context_set = intent.get('context_set')
            if context_set:
                if label not in label_context_sets:
                    label_context_sets[label] = []  # Initialize an empty list for the label if it doesn't exist
                label_context_sets[label].append(context_set)  # Append the context_set to the list for the label

    # Split and get name only from the context_set values
    #label_context_sets = {k: [v.split()[0] for v in vs] for k, vs in label_context_sets.items()}'''

     # Retrieve context_set for the given label
    label_context_sets = []
    for intent in intents['intents']:
        if 'tag' in intent and intent['tag'] == id2label[label]:
            context_set = intent.get('context_set')
            if context_set:
                label_context_sets.append(context_set)

    # Split and get name only from the context_set values
    label_context_sets = [context_set.split()[0] for context_set in label_context_sets]
    # Join the elements of the list into a single string and split it again to get a clean list
    label_context_sets = ' '.join(label_context_sets).split()

    collector(label_context_sets)

    
    return all_responses
    

    #response = random.choice(intents['intents'][label]['responses'])
        
    #print(f"smartgrader: {response}\n\n")
    #return response

def check_answer(question, answer):
    # User's answer stored in 'answer1' variable
    user_answer = answer
    all_responses = ai_model(question)

    # AI model's answer
    # Now you can use all_responses as needed
    for response in all_responses:
        ai_model_answer = response

        # Tokenize and vectorize the texts
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([user_answer, ai_model_answer])

        # Compute cosine similarity between the two vectors
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        # Set a threshold for similarity
        threshold = 0.4  # You can adjust this threshold as needed(0.8 preferred)

        # Compare similarity with threshold
        if similarity >= threshold:
            return  "Correct"
        

    return "InCorrect" 

'''def extract_questions_from_text(extracted_text):
    questions = []
    answers = []
    i = 1
    while True:
        question_match = re.search(rf'{i}\.(.*?)\n(.*?)\n', extracted_text, re.DOTALL)
        if question_match is None:
            break
        else:
            question_text = question_match.group(1).strip() # add questions
            questions.append(question_text)
            answer_match = question_match.group(2).strip() # add questions
            answers.append(answer_match)
            print(f"Question {i}: {question_text}")
            print(f"Answers {i}: {answer_match}")
            i += 1
    return questions, answers'''

import re

def extract_questions_from_text(extracted_text):
    questions = []
    answers = []

    # Define the regular expression pattern to match questions and answers
    question_pattern = r'(\d+)\. (.*?)\n'
    answer_pattern = r'Answers\n([\s\S]*)'

    # Find all question matches
    question_matches = re.findall(question_pattern, extracted_text)

    # Iterate through question matches
    for question_match in question_matches:
        question_number, question_text = question_match
        questions.append(question_text.strip())
        print(f"Question {question_number}: {question_text.strip()}")

    # Find the answer match
    answer_match = re.search(answer_pattern, extracted_text)
    if answer_match:
        answer_text = answer_match.group(1).strip()
        # Split the answer text into separate answers
        answer_texts = answer_text.split('\n')
        # Remove empty lines and append to the answers list
        answers.extend([answer.strip() for answer in answer_texts if answer.strip()])
        # Print the answers
        for i, answer in enumerate(answers, start=1):
            print(f"Answer {i}: {answer}")

    # Ensure checks has at least two elements before accessing checks[1]

    # Get the divide index
    divide_index = len(questions) // 2

    # Divide the questions array into two parts
    first_part = questions[:divide_index]
    second_part = questions[divide_index:]

    # Clear the question array
    questions.clear()

    # Insert everything into the answers array
    questions.extend(first_part)
    answers.extend(second_part)
    print(answers)

    return questions, answers


def get_data(extracted_text):
    checks = []
    questions, answers = extract_questions_from_text(extracted_text)

    for question, answer in zip(questions, answers):
        data = check_answer(question, answer)
        checks.append(data)

    return checks

def get_percentage(data):
    total_questions = len(data)
    correct = data.count('Correct')
    percentage = (correct / total_questions) * 100
    return percentage
