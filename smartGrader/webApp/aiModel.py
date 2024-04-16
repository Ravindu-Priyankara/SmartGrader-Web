
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
        threshold = 0.8  # You can adjust this threshold as needed

        # Compare similarity with threshold
        if similarity >= threshold:
            return  "Correct"
        

    return "InCorrect"

def extract_questions_from_text(extracted_text):
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
            i += 1
    return questions, answers

def get_data(extracted_text):
    checks = []
    questions, answers = extract_questions_from_text(extracted_text)

    for question, answer in zip(questions, answers):
        data = check_answer(question, answer)
        checks.append(data)

    return checks