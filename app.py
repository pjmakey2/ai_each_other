from flask import Flask, render_template, request
from random import choice
from settings import settings as sts
import openai
from bardapi import Bard
import re
from topics import topics

sts.OPEN_AI_MODEL
sts.OPEN_AI_TOKEN
sts.BARD_AI_TOKEN
#reg = r"```(?:.*?[\n])?([\s\S]*?)```"
reg = r"\^(?:.*?[\n])?([\s\S]*?)\^"

app = Flask(__name__)

openai.api_key  = sts.OPEN_AI_TOKEN

token = sts.BARD_AI_TOKEN
bard = Bard(token=token)

def get_completion(prompt: str, role: str):
    #role could be user, system, assistant
    messages = [{"role": role, "content": prompt}]
    response = openai.ChatCompletion.create(
        model=sts.OPEN_AI_MODEL,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

@app.route('/')
def AiEachOther():
    return render_template('AiEachOtherUi.html')

@app.route('/get_dialogue', methods=['POST'])
def GetDialogue():
    field = choice(topics)
    gtext = f"""Give me a topic for a dialogue in the field of "{field}". The topic has to be surrounded by the character ^."""
    print(gtext)
    rsp = get_completion(gtext, "user")
    print(rsp)
    rsp = re.findall(reg, rsp.replace('^:', ''))[0]
    return {'ai_qa': rsp, 'llm': choice(['chatgpt', 'bard']) }

@app.route('/get_q', methods=['POST'])
def GetQuestion():
    text = request.form.get('text')
    llm = request.form.get('llm')
    txtf = f"""
    Formulate a question base on the following text that are surrounded by the character ^ \
    ^{text}^ \
    Do not output other thing than the question, don't be polite. \
    Just output the question. \
    Your question has to be surrounded by the character ^ \
    Do not elaborate your answer
    """
    rsp = '```None```'
    if llm == 'chatgpt':
        rsp = get_completion(txtf, "user")
    if llm == 'bard':
        rsp = bard.get_answer(txtf)['content']
    print(llm)
    print(rsp)
    rsp = re.findall(reg, rsp.replace('^:', ''))[0].strip('```')
    return {'ai_qa': rsp, 'llm': llm }

@app.route('/get_answer', methods=['POST'])
def GetAnswer():
    text = request.form.get('text')
    text = f"""Answer the question surrounded by the character ^. \
               Your answer should have 150 characters or less ^{text}^.\
               Your given answer has to be surrounded by the character ^.\
               Do not eloborate at all just give me the answer.
            """
    
    llm = request.form.get('llm')
    llm_t = {
        'chatgpt': 'bard',
        'bard': 'chatgpt',
    }
    llmc = llm_t.get(llm)
    rsp = '```None```'
    if llmc == 'chatgpt':
        rsp = get_completion(text, "user")
    if llmc == 'bard':
        rsp = bard.get_answer(text)['content']
    print(llmc)
    print(rsp)
    rt = re.findall(reg, rsp.replace('^:', ''))
    if rt: 
        rsp = rt[0].strip('```')
    return {'ai_qa': rsp, 'llm': llm, 'llmc': llmc }
    
if __name__ == '__main__':
    app.run()

# You are now who making questions, give any random question, do not output other thing than the question    