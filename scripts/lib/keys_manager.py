import os 

class keys_manager:

    @staticmethod
    def setup():
        os.environ['OPENAI_API_KEY']=keys_manager.OPEN_AI_KEY
        os.environ['DASHCOPE_API_KEY']=keys_manager.ALI_API_KEY

    OPEN_AI_KEY = ""

    ALI_API_KEY = ""