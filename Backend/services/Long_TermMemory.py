from flask import Flask,request,jsonify
from Backend.extensions import db
from Backend.models.Conversation import Conversation
from Backend.models.Messages import Message 

def LongTermMemory(history, user_id, video_id):
    try:
        '''bulding the long term memory for the user so chatbot can remember the user details 
        and what is it pattern'''

        

        
    except Exception as e :
        print("there is an error in LongTermMemory route", e)
