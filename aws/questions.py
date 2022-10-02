import requests
from bs4 import BeautifulSoup
Q_API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-question-generation-ap"
A_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN_HERE"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_question(text):
    payload = "input:" + text
    response = requests.post(Q_API_URL, headers=headers, json=payload)
    question = response.json()[0]['generated_text']
    if question[-1] != "?":
        question = question + "?"
    return question

def generate_answer(question, context):
    payload = {
        "inputs" : {
            "question" : question,
            "context" : context
        }
    }
    response = requests.post(A_API_URL, headers=headers, json=payload)
    return response.json()['answer']

def get_text(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.get_text()

def split_and_filter(text, filter_length=200):
    filtered_by_length = [elem for elem in text.split("\n") if len(elem) > filter_length]
    allowed_characters = set("abcdefghijklmnopqrstuvwxyz'\",;.!?$()-—–[]0123456789 ")
    res = []
    for sentence in filtered_by_length:
        if set(sentence.lower()).issubset(allowed_characters):
            res.append(sentence.strip())
    return res


def get_questions(URL):
    URL = URL[1:-1]
    text = get_text(URL)
    sentences = split_and_filter(text)
    sentences = sentences[:3] # Rate limit hack
    questions = [generate_question(sentence)[10:] for sentence in sentences]
    # answers = [generate_answer(question, context) for question, context in zip(questions, sentences)]
    return questions
