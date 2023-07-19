import openai
from .config import settings


OPENAI_KEY = settings.openai_key

openai.api_key = OPENAI_KEY


def get_question():

    messages = []

    SYSTEM_ROLE_QUESTION = """
    You are a HR specialist that hires Junior React Developers.
    Your tasks are to ask questions both technical and behavioral to find \
    whether a person is a good fit or not to a company
    """
    messages.append({"role": "system","content": SYSTEM_ROLE_QUESTION})

    messages.append({"role": "user", "content": "Generate me just a \
                     question without any comments"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = completion["choices"][0]["message"]["content"]

    return reply


def get_score(question, answer):
    SYSTEM_ROLE = """
    You are a HR specialist that is looking for Junior React Developer. \
    You have a question and the answer that an applicant gave you. \
    Your task is to evaluate whether this candidate has answered this \
    question correctly in the scale from 0 (poorly) to 10 (fantastically). \
    Provide no comments, only a number. You need the return just a score.
    """
    prompt = f"""
        Question:{question}
        Answer: {answer} 
        Provide me a score, just a number, without any comments """

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_ROLE},
                {"role": "user", "content": prompt}]
        )
    reply = response["choices"][0]["message"]["content"]

    return reply
