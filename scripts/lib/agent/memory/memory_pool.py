from lib.mglobal.global_function import Global
from .mem_event import MemEvent
from lib.task.task_llm import LLMTaskFunction
from .memory_lib import MemLib
from settings import GlobalSettings

class MemoryPool:
    def __init__(self,agent_obj):
        self.agent_id=agent_obj.get_id()
        self.agent_name=agent_obj.get_name()
        self.lang=agent_obj.get_lang()
        # path
        storage_path=Global.get_storage_path(sub_folder=self.agent_id)
        self.memory_path=f"{storage_path}/memory.json"
        self.embedding_path=f"{storage_path}/embedding"
        
        # memory event
        self.events=dict()
        self.events['chat']=[]
        
        self.event_count=0
        pass
    
    def get_all_event_count(self):
        return self.event_count
    
    def get_event_count_by_type(self,type):
        if type in self.events:
            return len(self.events[type])
        return 0
    
    ################### File System #################
    def to_json(self):
        result={
            'basic_info':{
                'agent':self.agent_id,
                'event_count':self.event_count
            }
        }
        
        for type in self.events:
            result[type]=[x.encode() for x in self.events[type]]
            
        return result
    
    def flush_all(self):
        Global.json_update(self.memory_path,self.to_json())
        
    ################## Embedding ######################
    def save_embedding(self,memEvent,useEmbedding=False):
        path=f"{self.embedding_path}/{memEvent.embedding}.json"
        content=memEvent.to_content(self.lang)
        
        if useEmbedding:
            embedding=LLMTaskFunction.embedding(content,False)
        else:
            embedding=[0.5]*1536
        data={'data':embedding}
        Global.json_save(path,data)
        
    def get_embedding(self,memEvent):
        path=f"{self.embedding_path}/{memEvent.embedding}.json"
        if Global.check_if_file_exists(path):
            data=Global.json_load(path)
            if 'data' in data:
                return data['data']
        return [0.5]*1536
    
    ################### save event #####################
    def save_chat(self,agent_obj,content,importance=50.0,useEmbedding=False):
        agend_id=agent_obj.get_id()
        agent_name=agent_obj.get_name()
        lang=agent_obj.get_lang()
        timestamp=Global.get_global_now_time_stamp()
        type='chat'
        me=MemEvent.create_chat(pool=self,
                                agent_obj=agent_obj,
                                content=content,
                                timestamp=timestamp,
                                lang=lang)
        
        me.set_importance(importance)
        self.save_embedding(me,useEmbedding)
        
        if not(type in self.events):
            self.events[type]=[]
        self.events[type].append(me)
        self.event_count+=1
        
    def save_event(self,type,sub,verb,obj,timestamp,key_list,importance,useEmbedding=False):
        if type is None:
            type = "default"
        if sub is None:
            sub=""
        if verb is None:
            verb=""
        if obj is None:
            obj=""
        if importance is None:
            importance=5.0
        if timestamp is None:
            timestamp=1000000
        if key_list is None:
            key_list=[]

        me=MemEvent.create(pool=self,
                           type=type,
                           sub=sub,
                           verb=verb,
                           obj=obj,
                           timestamp=timestamp)
        
        me.set_importance(importance)
        for key in key_list:
            if key in sub or key in verb or key in obj:
                me.keys.append(key)
        
        self.save_embedding(me,useEmbedding)
       
        if not(type in self.events):
            self.events[type]=[]
        self.events[type].append(me)
        self.event_count+=1
        
        
    ################ MEMORY SEARCH ##################
    def get_event_list_by_type(self,type_list):
        result=[]
        
        for type in type_list:
            if self.events.get(type) != None:
                result+=self.events.get(type)
        
        return result
    
    def search_recent_memory(self,type,time_step_range=5,count=5):
        # get events by type
        events=self.events.get(type,[])
        # filter by time step range
        now_time=Global.get_global_now_time_stamp()
        events=[e for e in events if (now_time-e.lastaccess) < time_step_range ]
        # # get importance
        # recency_score=MemLib.mem_extract_recency(events)
        # score_highest=MemLib.top_highest_x_values(recency_score,count)
        
        # # update latest access
        # self.update_latest_access(score_highest)
        
        recent_event=sorted(events,
                            key=lambda x:x.timestamp,
                            reverse=True)[:count]
        self.update_latest_access(recent_event)
        
        return recent_event
        
    
    def search_most_relative_memory(self,type_list,focus_content=None,time_step_range=5,count=5):
        """
        Search for the most latest memory, and return the most relative memory events

        Args:
            type_list (List[string]): the list of types ('chat','thought')
            focus_content (string, optional): return the focus content point, Defaults to None.
            time_step_range (int, optional): the consider time step range. Defaults to 5.
            count (int, optional): the memory event to collect. Defaults to 5.

        Returns:
            searched event list (List[MemEvent]): the result memory events
        """
        events_by_type=self.get_event_list_by_type(type_list)
        
        # filter by time step
        now_time=Global.get_global_now_time_stamp()
        events=[e for e in events_by_type if (now_time-e.lastaccess) < time_step_range ]
        
        event_dict=MemLib.mem_generate_event_dict(events)
        
        # get the score by importance, recency and focus_content relevance
        recency_score=MemLib.mem_extract_recency(events)
        imprtance_score=MemLib.mem_extract_importance(events)
        favor_score=MemLib.mem_extract_favor(events)
        if focus_content!=None:
            ref_embedding=LLMTaskFunction.embedding(focus_content,False)
            relevance_score=MemLib.mem_extract_relevance(events,self,ref_embedding)
            
        # get the weight from the score dictionary   
        weight=[0.5,2,2,1]
        final_score={}
        
        if focus_content!=None:
            for key in recency_score.keys():
                final_score[key]=(
                    recency_score[key]*weight[0]
                    +  imprtance_score[key]*weight[1]
                    + favor_score[key]*weight[2]
                    + relevance_score[key]*weight[3]
                )
        else:
            for key in recency_score.keys():
                final_score[key]=(
                    recency_score[key]*weight[0]
                    + imprtance_score[key]*weight[1]
                    + favor_score[key]*weight[2]
                )
                
        # 
        score_highest=MemLib.top_highest_x_values(final_score,count)
        high_events=[event_dict[key] for key in list(score_highest.keys())]

        self.update_latest_access(high_events)
        
        return high_events
        
    def update_latest_access(self,event_list):
        """
        update the latest access of the memory event

        Args:
            event_list (List[MemEvent]): let the event list update the 
                                        lastaccess to now time stamp
            
        """
        
        if GlobalSettings.UPDATE_LAST_ACCESS:
            time=Global.get_global_now_time_stamp()
            for e in event_list:
                etype=e.type
                index=e.type_id
                self.events[etype][index].lastaccess=time
        
    def update_chat_favor(self,favor_dict):
        type='chat'
        events_by_type=self.get_event_list_by_type([type])
        
            
        for event in events_by_type:
            id = event.type_id
            agent=event.subject
            
            favor=favor_dict.get(agent)
            if favor != None:
                self.events[type][id].favor=favor
            
        