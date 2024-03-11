from fastapi import APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import InitializeData, ChatData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from connections.mongo_db import db_client
from datetime import datetime
from openai import OpenAI
from Constants.utils import get_chat_history_buffer_memory
from gpt4all import GPT4All
from pathlib import Path
import os
import bs4
from langchain_openai import OpenAI as oai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)
cli = oai(base_url="https://c8db-115-244-132-22.ngrok-free.app/v1", api_key="not-needed")
mydir = os.path.join(os.getcwd(),'data','ayurvedha.txt')
name = ""
loader = TextLoader(mydir, autodetect_encoding=True)
data = loader.load()
print("splitting text and embedding using gpt4all embeddings")
data[0].metadata = {'keywords': 'some random metadata'}
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=splits, embedding=GPT4AllEmbeddings())
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = cli

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def enter_question(question):
    print("about to invoke the rag_chain")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print(rag_chain)
    # question = input("Enter your prompt: ")
    l=[]
    for chunk in rag_chain.stream(question):
        l.append(chunk)
    return "".join(l)

def check_for_words(string, word_list=["hgdhfdhgfsgsgdasgrs"]):
    for word in word_list:
        if word in string:
            return True
    return False


def generate_chat_completion(data):
    room_id = data["userid"]+"1234"
    prompt = data["query"]
    if check_for_words(prompt):
        if prompt == "":
            return ""
        # conversation_response = enter_question(prompt[:-2])
    else:
        
        room_data = db_client.get_last_history(room_id, 100)
        conversation_length = 0 if room_data is None else (len(room_data['history']) - 1)//2
        # print(room_data)
        k=0
        if room_data is None:
            prompt = "Please ask me question to find out necessary symptoms. I would prefer you use symptom questions one at a time. Use short questions"
            k=1
            new_room_data = {
                'roomid': room_id,
                'followUpQuestions': None,
                'history': [
                    {'role': "system", 'content': "You are a calm dermatology assistant. Keep the responses short. Assume that the user does not understand dermatology so try to explain the terms. Ask the patient about symptoms prefered only one question at a time, validate the model predictions and give a preliminary diagnosis. If the user's symptoms don't match to any of the diseases, explain that if they still feel sick to visit a dermatologist. Do not ask the user to decide the disease only ask about symptoms and decide on your own. Four models gives the following output for the patient where keys under 0 is more relevant than those under 1 are less revelent. Only ask question to confirm the disease from these possibilities: " + str(db_client.get_user_data(data["userid"])["diagnosis"]), 'timestamp': str(datetime.now())},
                ],
                'conversation_history': [
                    {'role': "assistant", 'content': "You are a dermatology assistant.", 'timestamp': str(datetime.now())},
                ],
            }

            db_client.create_room(new_room_data)
            room_data = db_client.get_last_history(room_id, 100)
        his_data = room_data["history"][1:]
        base_system = [{'role': "system", 'content': """You are a smart dermatology assistant. Keep the responses short. Assume that the user does not understand dermatology so try to explain the terms. Do not ask the user to decide the disease only ask about symptoms and decide on your own. Ask the patient about symptoms, validate the model predictions and give a preliminary diagnosis.  If the user's symptoms don't match to any of the diseases, explain that if they still feel sick to visit a dermatologist. Four models gives the following output for the patient where keys under 0 is more relevant than those under 1 are less revelent. Only ask question to confirm the disease from these possibilities: """ + str(db_client.get_user_data(data["userid"])["diagnosis"])}]
        if k==0:
            message = base_system + [{'role': entry['role'], 'content': entry['content']} for entry in his_data[-20:]]
        else:
            message = base_system
        message.append({'role': "user", 'content': prompt})
        print(message)
        client = OpenAI(base_url="https://c8db-115-244-132-22.ngrok-free.app/v1", api_key="not-needed")
        completion = client.chat.completions.create(
        model="local-model",
        messages= message,
        temperature=0.7,
        )

        print(completion.choices[0].message)
        conversation_response = completion.choices[0].message.content
        if conversation_response == "":
            conversation_response = "513 Bad response"
    history = [
        {'role': "user", 'content': prompt, 'timestamp': str(datetime.now())},
        {'role': "assistant", 'content': conversation_response, 'timestamp': str(datetime.now())},
    ]
    db_client.append_message_to_room(room_id, history,str(datetime.now()))
    
    return conversation_response


@router.post("/initialize")
async def intialize_user_chat(data: InitializeData = Body(..., description="Image data")):
    response = data
    
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response)

@router.post("/query")
async def chat_completion(data: ChatData = Body(..., description="Image data")):
    response = generate_chat_completion(data.dict())
    # response = dict(db_client.get_user_data(data.userid))
    # del response["_id"]
    print("Outside")
    print(response)
    print()
    # return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response)
    return response