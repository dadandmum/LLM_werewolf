from settings import GlobalSettings
from lib.mglobal.global_function import Global
from lib.agent.memory.memory_pool import MemoryPool
from .persona.big_five import BigFivePersona

class AgentDescription:
    def __init__(self,description,presence_penalty,temperature) -> None:
        self.description=description
        self.presence_penalty=presence_penalty
        self.temperature=temperature

class MAgent:
    def __init__(self,_agent_id,debug=None):
        self.agent_id=_agent_id
        self.session=GlobalSettings.SESSION
        
        # init info 
        agent_info=Global.load_agent_info(self.agent_id)
        self.name=agent_info.get('name')
        self.lang=agent_info.get('language')
        self.info=agent_info
        self.use_embedding=GlobalSettings.USE_EMBEDDING
        
        # descripiton
        self.description=dict()
        # self.description['default']=agent_info.get('default','')
        self.description['default']='You are a player.'
        if GlobalSettings.UES_RANDOM_BIG_FIVE:
            (trait,bf_desc)=BigFivePersona.get_rand_big_five_description()
            self.description['bigfive']=f"You are {self.get_name()}. {bf_desc}"
            self.bf_trait=trait
        
        if debug is None:
            self.debug=GlobalSettings.DEBUG_LOG & GlobalSettings.DEBUG_LOG_AGENT
        else:
            self.debug=debug
        
        # init memory
        self.memory=MemoryPool(self)
        
    ################ Memory ###################
    def flush_memory(self):
        self.memory.flush_all()
        
    def events_to_content(self,event_list)->str:
        event_content_list=[e.to_content(lang=self.lang) for e in event_list]
        return ";".join(event_content_list)
    
    def find_most_recent_memory(self,type,time_step_range=5,count=5):
        events = self.memory.search_recent_memory(type,time_step_range,count)
        return self.events_to_content(events)
    
    def find_most_relative_memory(self,type_list,time_step_range=5,count=5):
        events = self.memory.search_most_relative_memory(type_list=type_list,time_step_range=time_step_range,count=count)
        return self.events_to_content(events)
    
    ############### Interaction ###############
    def remember(self,type,sub,verb,obj,key_list,importance)->None:
        time_stamp=Global.get_global_now_time_stamp()
        self.memory.save_event(type,sub,verb,obj,time_stamp,key_list,importance,self.use_embedding)
    
    def update_chat_favor(self,favor_dict)->None:
        self.memory.update_chat_favor(favor_dict)
    
    ################ Information ##############
    def get_id(self)->str:
        return self.agent_id
    
    def get_name(self)->str:
        return self.name
    
    def get_lang(self)->str:
        return self.lang
    
    def get_info_key(self,key)->str:
        return self.info.get(key,'')
    