import os
import sys
from settings import GlobalSettings
import lib.keys_manager as keys_manager
from lib.chat_model.llm_chat_model import ChatModel

class LLMChecker:
    def __init__(self,argv)->None:
        pass 

    def run(self):
        messages=[
            {'role':'system','content':'You are a kindful assistant.'},
            {'role':'user', 'content':'Who are you?'}
        ]
        param={
            'temperature' : 1.2,
            'frequency_penalty' : 1.2,
        }
        llm_model = GlobalSettings.LLM_MODEL_DICT['default']
        chat_model=ChatModel(model=llm_model,debug=True)
        response=chat_model.send(messages,param)

        print(f">> Response is [{response['content']}] << ")

