class ChatModelBase:
    def __init__(self,_model="gpt-3.5",debug=False) -> None:
        self.model = _model
        self.debug=debug
        if self.debug:
            print(f"init chat model -> {_model}")

    def send(self,message,param,debug=False):
        pass

    def get_embedding(self,content,debug=False)->list:
        pass