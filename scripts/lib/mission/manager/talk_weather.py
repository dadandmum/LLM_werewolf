from lib.mission.mission_base import MissionBase
from lib.task.task_llm import LLMTaskFunction
from lib.language.language_dict import LanguageDict
from lib.mglobal.global_function import Global
import random


class TalkWeatherInfo:
    def __init__(self,agent_id,main,personal):
        self.agent_id=agent_id
        self.main=main
        self.personal=personal
        
    def to_content(self):
        return f"{self.main}. {self.personal}"
        
class TalkWeather(MissionBase):
    def __init__(self, mission_name,mission_file=None, debug=True):
        super(TalkWeather,self).__init__(mission_name, mission_file,debug)
        mission_info=Global.load_mission_info(self.mission_name)
        self.weathers=mission_info.get('weather_list',['Sunny'])
        self.main=mission_info.get('description')
        self.personal=mission_info.get('personal')
        
    def start_mission(self, env_info):
        super().start_mission(env_info)
        self.talk_index=0
        self.mission_infos=[]
        for agent in self.agents:
            personal=self.personal.replace('<WEATHER>',random.choice(self.weathers))
            info=TalkWeatherInfo(agent.get_id(),self.main,personal)
            self.mission_infos.append(info)
            
    def get_mission_content(self, agent_id) -> str:
        info=[x for x in self.mission_infos if x.agent_id==agent_id]
        if len(info)>0:
            info=info[0]
            return info.to_content()
        return ""
        
    def get_mission_name(self) -> str:
        return 'TalkWeather'
    
    def next_step(self, step_index):
        super().next_step(step_index)
        
        talk_agent=self.agents[self.talk_index]
        self.talk_index=(self.talk_index+1) % len(self.agents)
        
        result=LLMTaskFunction.generate_dialog(talk_agent,self)
        content=result.get('content','')
        
        print(f"[TalkWeather] (dialog{step_index}) \n {talk_agent.get_name()} says: {content}\n")
        LLMTaskFunction.boardcast_chat(self.agents,
                                       talk_agent,
                                       content )
        
        for agent in self.agents:
            agent.flush_memory()
            
    def check_end_mission(self) -> bool:
        return self.time_stamp > 5