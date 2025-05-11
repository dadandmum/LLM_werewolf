
from lib.mglobal.global_function import Global
from settings import GlobalSettings
from lib.task.task_llm import LLMTaskFunction
from numpy import dot
from numpy.linalg import norm
import numpy as np

class AnalyzeRecorder:
    def __init__(self,mission):
        self.mission=mission
        self.session=mission.session
        self.dialog_record=[]
        self.time_record=[]
        self.vote=[]
        
    def get_analyze_root(self):
        return Global.get_storage_path('analyze')
    
    def record_dialog(self,agent_obj,mission_info,dialog):
        log_file=f"{self.get_analyze_root()}/dialog.json"
        time=Global.get_now_time_in_YMD_HMS()
        time_stamp=self.mission.get_time_stamp()
        agent_name=agent_obj.get_name()
        agent_id=agent_obj.get_id()
        embedding_tag=f"{agent_id}-{time_stamp}-dialog"
        personal_mission=mission_info.mission_personal
        role=mission_info.self_role
        trait='none'
        if hasattr(agent_obj,'bf_trait'):
            trait=agent_obj.bf_trait
        
        embedding=LLMTaskFunction.embedding(dialog,False)
        embedding_path=f"{self.get_analyze_root()}/embedding/{embedding_tag}.json"
        
        Global.json_save(embedding_path,{'data':embedding})
        
        Global.json_add_item_to_list(log_file,'record',{
            'time':time,
            'time_stamp':time_stamp,
            'sender_name':agent_name,
            'sender_id':agent_id,
            'sender_role':role,
            'sender_personal':personal_mission,
            'dialog':dialog,
            'trait':trait,
            'embedding_tag':embedding_tag
        })
        
        self.dialog_record.append({
            'time':time,
            'time_stamp':time_stamp,
            'sender_name':agent_name,
            'sender_id':agent_id,
            'sender_role':role,
            'dialog':dialog,
            'trait':trait,
            'embedding':embedding,   
        }
        )
        
    def record_time(self,agent_obj,time_dict):
        log_file=f"{self.get_analyze_root()}/time.json"
        
        time=Global.get_now_time_in_YMD_HMS()
        time_stamp=self.mission.get_time_stamp()
        agent_name=agent_obj.get_name()
        agent_id=agent_obj.get_id()
        
        data={
            'time':time,
            'time_stamp':time_stamp,
            'sender_name':agent_name,
            'sender_id':agent_id,
            'time_use':time_dict
        }
        
        Global.json_add_item_to_list(log_file,'record',data)
        
        self.time_record.append(data)
        
    def record_vote(self,vote_dict,turn):
        log_file=f"{self.get_analyze_root()}/vote.json"
        
        time=Global.get_now_time_in_YMD_HMS()
        time_stamp=self.mission.get_time_stamp()
        
        data={
            'time':time,
            'time_stamp':time_stamp,
            'turn':turn,
            'vote':vote_dict
        }
        Global.json_add_item_to_list(log_file,'record',data)
        self.vote.append(data)
        
        
    def record_favor(self,favor_dict):
        log_file=f"{self.get_analyze_root()}/favor.json"
        
        time=Global.get_now_time_in_YMD_HMS()
        time_stamp=self.mission.get_time_stamp()
        
        data={
            'time':time,
            'time_stamp':time_stamp,
            'favor':favor_dict,
        }
        Global.json_add_item_to_list(log_file,'record',data)
        
        
    def final_analyze(self):
        self.final_analyze_dialog(self.dialog_record,f"{self.get_analyze_root()}/dialog_final.json")
        
    @staticmethod
    def final_analyze_dialog(dialog_record,output):
        # analyze overall diff 
        result=dict()
        turn=GlobalSettings.TALK_TURN
        
        # get overall difference 
        result['overall']=AnalyzeRecorder.get_difference_of_dialog_list_by_turn(dialog_record,turn)
        
        # get difference for each agent
        # agents=list(set([x['sender_id'] for x in dialog_record]))
        # agent_result=dict()
        # for agent in agents:
        #     ar=AnalyzeRecorder.get_difference_of_dialog_list([x for x in dialog_record if x['sender_id']==agent])
        #     ar['agent']=agent
        #     agent_result[agent]=ar
        # result['agents']=agent_result
        
        
        log_file=output
        Global.json_save(log_file,result)
        return result
    
    @staticmethod
    def analyze_dialog_by_agent(dialog_record,output):
        result=dict()
        # get difference for each agent
        agents=list(set([x['sender_id'] for x in dialog_record]))
        agent_result=dict()
        for agent in agents:
            ar=AnalyzeRecorder.get_difference_of_dialog_list([x for x in dialog_record if x['sender_id']==agent])
            ar['agent']=agent
            agent_result[agent]=ar
        result['agents']=agent_result
        
        Global.json_save(output,result)
        return result
        
        
    @staticmethod  
    def get_difference_of_dialog_list(dialog_list):
        vector_list=[dialog_list[i]['embedding'] for i in range(len(dialog_list))]
        result=AnalyzeRecorder.analyze_vector(vector_list)
        return result
        
    @staticmethod  
    def get_difference_of_dialog_list_by_turn(dialog_list,turn=1):
        turn_list=[]
        total_turn=turn
        total_agent=len(dialog_list)/total_turn
        
        for t in range(total_turn):
            step_count=int((t+1)*total_agent)
            vector_list=[dialog_list[i]['embedding'] for i in range(step_count) ]
            result=AnalyzeRecorder.analyze_vector(vector_list)
            turn_list.append({'index':t,'step':step_count,'result':result})
        
        return turn_list
    
    @staticmethod
    def analyze_vector(vector_list):
        # mean 
        data=np.array(vector_list)
        # mean=data.mean(axis=0)
        
        # distance_vector=np.array([ AnalyzeRecorder.distance(mean,x) for x in data ])
        distance_vector=[]
        count=len(data)        
        for i in range(count):
            for j in range(count):
                if i != j:
                    x=data[i]
                    y=data[j]
                    distance_vector.append(AnalyzeRecorder.distance(x,y))
        distance_vector=np.array(distance_vector)
        
        dis_mean=distance_vector.mean()
        dis_std=distance_vector.std()
        dis_var=distance_vector.var()
        
        return {
            'mean' : float(dis_mean),
            'std'  : float(dis_std),
            'var'  : float(dis_var)
        }
            
    
    
    @staticmethod
    def distance(a,b):
        return 1 - AnalyzeRecorder.cos_sim(a,b)
        # return np.linalg.norm(a-b)
    
    @staticmethod
    def cos_sim(a,b):
        """
        This function calculates the cosine similarity between two input vectors
        'a' and 'b'. Cosin similarity is a measure of similarity between two
        non-zero vectors of an inner product space that measures the cosine
        of the angle between them.

        Args:
            a (_type_): 1-D array object
            b (_type_): 1-D array object

        Returns:
            A scalar value representing the cosine similarity between the input
            vectors 'a' and 'b'
            
        Example input:
            a = [0.2,0.3,0.4]
            b = [0.3,0.2,0.4]
        """
        return dot(a,b)/(norm(a)*norm(b))