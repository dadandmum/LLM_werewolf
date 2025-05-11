import sys

from settings import GlobalSettings
from lib.chat_model.openai.openai_model import OpenAIModel
from lib.chat_model.qwen.qwen_model import TongyiChat

class ChatModel:

    def __init__(self,model=None,ebmodel=None,debug=None)->None:
        # init model 
        self.model=GlobalSettings.LLM_MODEL
        if not(model is None):
            self.model=model

        # init debug 
        # if debug is not set or debug is required 
        if debug is None or debug == True: 
            self.debug = GlobalSettings.DEBUG_LOG and GlobalSettings.DEBUG_LOG_LLM
        else : # if debug is not required
            self.debug = False

        if self.model.startswith('gpt'):
            self.chat_model=OpenAIModel(self.model,self.debug)
        elif self.model.startswith('qwen'):
            self.chat_model=TongyiChat(self.model,self.debug)


        # if ebmodel is None:
        self.embedding_model=OpenAIModel(GlobalSettings.LLM_EMBEDDING_MODEL,self.debug)

    def send(self,msg,param)->dict:
        if param is None:
            param={}
        if self.debug:
            print(f"-- Send LLM Request [{self.model}]--")
            print({'msg':msg,**param})

        response = self.chat_model.send(msg,param,self.debug)

        if self.debug:
            print(f"== Response LLM Requese [{self.model}]")
            print(response)

        return response
    

    def get_embedding(self,content,debug=False) -> list:
        response=self.embedding_model.get_embedding(content,debug)
        return response