from lib.mglobal.global_function import Global
from lib.language.language_dict import LanguageDict

class MemEvent:
    def __init__(self,id,type_id,type,time,timestamp,agent,sub,verb,obj):
        # basic data 
        self.id=id
        self.type_id=type_id
        self.type=type
        self.time=time
        self.timestamp=timestamp
        self.lastaccess=timestamp
        self.agent=agent
        self.subject=sub
        self.verb=verb
        self.object=obj
        # optional data 
        self.keys=[]
        self.tag=""
        self.embedding=""
        self.importance=5.0
        self.favor=5.0
        self.gen_embedding_key()
        
    def gen_embedding_key(self):
        self.embedding=f"{self.id}-{self.timestamp}"
        return self.embedding
    
    def encode(self):
        """
        Turn self to a dict(json) node
        """
        result={}
        # basic data
        result['id']=self.id
        result['type_id']=self.type_id
        result['type']=self.type
        result['time']=self.time
        result['timestamp']=self.timestamp
        result['lastaccess']=self.lastaccess
        result['agent']=self.agent
        result['subject']=self.subject
        result['verb']=self.verb
        result['object']=self.object
        
        # optional data
        result['tag']=self.tag
        result['keys']=self.keys
        result['embedding']=self.embedding
        result['importance']=self.importance
        result['favor']=self.favor
        
        return result
    
    def set_importance(self,importance):
        if importance != None:
            self.importance= max(0.0 , min( importance , 100.0))
    
    @staticmethod
    def decode(json):
        event=MemEvent(json['id'],
                       json['type_id'],
                       json['type'],
                       json['time'],
                       json['timestamp'],
                       json['agent'],
                       json['subject'],
                       json['verb'],
                       json['object'])
        
        event.lastaccess=json.get('lastaccess',event.timestamp)
        event.tag=json.get('tag','')
        event.keys=json.get('keys',[])
        if 'embedding' in json:
            event.embedding=json.get('embedding')
        event.importance=json.get('importance',5.0)
        event.importance=json.get('favor',5.0)
        
        return event
    
    def to_content(self,withTime=False,lang='EN'):
        if withTime:
            at=LanguageDict.translate('at',lang)
            
            if self.type == 'chat':
                return f"{self.subject} {self.verb}:'{self.object}' {at} {self.time}"
            else:   
                return f"{self.subject} {self.verb} {self.object} {at} {self.time}"
        else:
            if self.type == 'chat':
                return f"{self.subject} {self.verb}:'{self.object}'"
            else:
                return f"{self.subject} {self.verb} {self.object}"
        
    @staticmethod
    def create(pool,type,sub,verb,obj,timestamp=None):
        time=Global.get_now_time_in_YMD_HMS()
        agent=pool.agent_name
        if timestamp is None:
            timestamp=Global.get_now_time()
        
        id=pool.get_all_event_count()+100000000
        type_id=pool.get_event_count_by_type(type)
        
        return MemEvent(id,type_id,type,time,timestamp,agent,sub,verb,obj)
    
    @staticmethod
    def create_chat(pool,agent_obj,content,timestamp=None,lang='EN'):
        verb=LanguageDict.translate('say',lang)
        sub=agent_obj.get_name()
        event=MemEvent.create(pool,'chat',sub,verb,f'"{content}"',timestamp)
        event.keys.append(agent_obj.get_id())
        return event
        
    