from .werewolf import Werewolf
from lib.task.task_llm import LLMTaskFunction
from settings import GlobalSettings
from lib.mglobal.global_function import Global
from lib.mission.mission_base import MissionBase
import random
import re 
import time 

class WerewolfB5P(Werewolf):
    def __init__(self, mission_name,mission_file=None, debug=True):
        super(WerewolfB5P,self).__init__(mission_name, mission_file, debug)
    
    def start_mission(self, env_info):
        super().start_mission(env_info)
        
        des_dict=self.mission_info.get('description_dict')
        tra_dict=self.mission_info.get('trait_dict')
        for agent in self.agents:
            id=agent.get_id()
            desctipion=des_dict.get(id)
            trait=tra_dict.get(id)
            agent.description['bigfive']=desctipion
            agent.bf_trait=trait
            
        self.log_record("[WerewolfB5P] >> Agent desc >>")
        for agent in self.agents:
            self.log_record(f"[Agent {agent.get_name()}]")
            self.log_record(agent.bf_trait)
            self.log_record(agent.description['bigfive'])
            
    def next_step(self, step_index):
        agent_key = 'bigfive'
        
        # self.log_debug(f">> Run Mission [{self.mission_name}] step [{step_index}]<<")
        # self.time_stamp=step_index
        # self.talk_index=step_index%self.player_count
        # self.round_index=step_index//self.player_count
        self.next_step_update_index(step_index)
        
        talk_agent=self.agents[self.talk_index]

        dialog=self.generate_single_talk(talk_agent,self,agent_key)

        if GlobalSettings.USE_ANALYZE:
            self.log_record("** Start Analayze **")
            start_time=time.time()
            self.analyze.record_dialog(talk_agent,self.get_info(talk_agent.get_id()),dialog)
            end_time=time.time()
            self.log_record(f"** End Analayze({end_time-start_time}s) **")
            
        for agent in self.agents:
            agent.flush_memory()
            
        self.log_record("[Werewolf] - End Next Step - ")
            
    def generate_single_talk(self,agent_obj,mission,agent_key):
        self.log_record("** Start Generate Single Talk **")
        
        response=LLMTaskFunction.generate_dialog(agent_obj=agent_obj,
                                                 mission=mission,
                                                 agent_desc_key=agent_key,
                                                 ignore_memory=True)
        time_use=response.get('time_use')
        self.log_record(f"** End Generate Talk (Time use:{time_use}s) **")
        
        # result=LLMTaskFunction.generate_dialog(talk_agent,self,agent_key)
        dialog=Global.clean_dialog_content(response.get('content',''),agent_obj.get_name())
        
        self.log_record(f"[Werewolf] (dialog({self.round_index},{self.talk_index})) \n {agent_obj.get_name()} says: {dialog}\n")
        
        # target_list=[agent_obj]
        # favor_dict_att=self.generate_favor_dict_agents_to_target(target_list,agent_obj)
        # LLMTaskFunction.boardcast_chat(target_list,
        #                                agent_obj,
        #                                dialog,
        #                                favor_dict_att)
        
        return dialog