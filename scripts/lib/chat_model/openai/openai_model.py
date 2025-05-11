from openai import OpenAI
from ..chat_model_base import ChatModelBase

# ref 
# https://platform.openai.com/docs/api-reference/chat

class OpenAIModel(ChatModelBase):
    def __init__(self, _model="gpt-3.5", debug=False) -> None:
        super(OpenAIModel,self).__init__(_model, debug)
        self.client=OpenAI()

    def send(self,msg,param,debug=False):
        if self.model is None:
            print(f"[Error] send LLM Request with None Model")
            return { 'error' : 'Send LLm Requeset with None Model'}
        
        frequency_penalty=param['frequency_penalty'] if 'frequency_penalty' in param else 0.0
        presence_penalty=param['presence_penalty'] if 'presence_penalty' in param else 0.0
        temperature = param['temperature'] if 'temperature' in param else 1.0
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=msg,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            temperature=temperature,
            stream=False,
        )

        if debug:
            print(f">>> completion {self.model}<<<")
            print(completion)
        
        result = {}
        result['content']=completion.choices[0].message.content
        result['role']=completion.choices[0].message.role

        return result
    
    
    def get_embedding(self, content,debug=False) -> list:
        if debug:
            print(f"[embedding[{self.model}]] Content is [{content}] ")
        
        response=self.client.embeddings.create(
            input=content,
            model=self.model
        )
        
        return response.data[0].embedding