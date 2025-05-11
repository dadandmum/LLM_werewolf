from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader

from ui.llm_tool_raw import Ui_MainWindow
from lib.mglobal.global_function import Global
from lib.task.task_llm import LLMTaskFunction
from lib.chat_model.llm_chat_model import ChatModel
from lib.agent.persona.big_five import BigFivePersona

import sys
import re


agent_list=["Alpha","Beta"]
agent_info_list=["bigfive","default","description"]
model_list=["qwen-plus","gpt-3.5-turbo-0125","gpt-4o","qwen2-72b-instruct","qwen1.5-110b-chat","gpt-4o-mini"]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # agent 
        self.agentCombo.addItems(agent_list)
        self.agentCombo.currentIndexChanged.connect(self.on_agent_changed)
        self.agentInfoCombo.addItems(agent_info_list)
        self.agentInfoCombo.currentIndexChanged.connect(self.on_agent_changed)
        
        self.on_agent_changed(0)
        
        # task
        self.taskCombo.addItems(LLMTaskFunction.get_all_tasks())
        self.taskCombo.currentIndexChanged.connect(self.on_task_changed)
        self.taskParameterText.textChanged.connect(self.on_parameter_chaged)
        
        self.on_task_changed(0)
        
        # self.on_parameter_chaged("")
        
        # model
        self.modelCombo.addItems(model_list)
        
        # confirm
        self.confirmButton.clicked.connect(self.on_confirm)
        
    def on_agent_changed(self,index):
        agent = self.agentCombo.currentText()
        info = self.agentInfoCombo.currentText()
        
        data = Global.load_agent_info(agent)
        
        if info == "bigfive":
            info_content=BigFivePersona.get_rand_big_five_description()[1]
        else:
            info_content = data.get(info,"")
        self.agentInfo.setPlainText(info_content)
        
    def on_task_changed(self,index):
        task = self.taskCombo.currentText()
        
        task_template=LLMTaskFunction.get_task_template(task)
        self.taskParameterText.setPlainText(self.get_init_keys(task_template))
        self.TaskFullText.setPlainText(task_template)
        
        self.on_parameter_chaged()
        
    def on_parameter_chaged(self):
        # get all parameters content
        task=self.taskCombo.currentText()
        param_text=self.taskParameterText.toPlainText()
        param_pattern='<(\w+)>-><(.*)>'
        param_pairs=re.findall(param_pattern,param_text)
        
        # get task prompt
        task=self.taskCombo.currentText()
        input={}
        for (key,value) in param_pairs:
            input[key]=value
            
        prompt=LLMTaskFunction.get_prompt(task,input)
        self.TaskFullText.setPlainText(prompt)
        
        
    def on_confirm(self):
        # get perpare for all llm parameters
        agent_name = self.agentCombo.currentText()
        info_type = self.agentInfoCombo.currentText()
        task=self.taskCombo.currentText()
        system_prompt=self.agentInfo.toPlainText()
        user_prompt=self.TaskFullText.toPlainText()
        model=self.modelCombo.currentText()
        msg=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role":"user",
                    "content":user_prompt
                }
            ]
        param=LLMTaskFunction.get_parm(agent_name,info_type)
        
        # response=LLMTaskFunction.call_model(task,agent_name,input,info_type,True)
        chat_model=ChatModel(model=model,debug=True)
        response=chat_model.send(msg,param)
        content=response.get('content')
        self.resultText.setPlainText(content)
        
        
    def get_init_keys(self,task_template):
        keys=LLMTaskFunction.get_keys_from_template(task_template)
        result = ""
        for key in keys:
            if key == "NAME":
                agent=self.agentCombo.currentText()
                result += f"<{key}>-><{agent}>\n"
            elif  "MEMORY" in key :
                fake_memory="Zeta say Agreed, let's proceed methodically. As a Villager, I value clear observation and logical reasoning. Alpha's support for me isn't inherently suspicious. We need more evidence and careful analysis of interactions. Delta's insights as Seer are crucial. For now, no one seems overtly suspicious. Let's continue to share thoughts tactfully, focusing on behaviors and patterns. Considering the impact of a Tanner is important. We must work together and maintain vigilance to identify the Werewolf.;Theta say Agreed, let's proceed methodically. As a Mason, my trust in Epsilon is inherent. Alpha's advocacy for Zeta stands out but isn't definitive. We need to gather more evidence and observe interactions closely. Zeta, your logical approach is valuable. Let's all continue to share insights while maintaining caution. For now, no player appears strongly suspicious, but we must remain vigilant. Observing how Alpha and Zeta interact could provide clues. We should also consider the potential impact of a Tanner.;"
                result += f"<{key}>-><{fake_memory}>\n"
            elif "MISSION" in key:
                fake_content="There are serval roles in the game: Werewolf, Minion, Seer, Mason, Tanner and Villager. Werewolf, Minon is part of evil team, Seer, Mason and Villager is part of the good team. Tanner is the third party. All players will speak in turn for several rounds. After the discussion rounds, players will vote to identify the Werewolf. If the Werewolf is voted out, the good team win. If a Villager or a Seer or a Mason is voted out, the Werewolf wins. If the Thinker is voted out, the Tanner wins and all the rest of players lose.You are Villager. You are part of good team. You need to find out who is the werewolf. "
                result +=f"<{key}>-><{fake_content}>\n"
            elif "AGENTS" in key:
                fake_content="Alpha;Beta;Gamma;"
                result +=f"<{key}>-><{fake_content}>\n"
            else:
                result += f"<{key}>->< >\n"
        
        return result

def run_tool():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()