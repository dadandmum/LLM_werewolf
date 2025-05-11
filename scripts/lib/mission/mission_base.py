from lib.mglobal.global_function import Global
from settings import GlobalSettings
from lib.agent.magent import MAgent
import re 

class MissionBase:  
    def __init__(self,mission_name,mission_file=None,debug=True):
        self.mission_name=mission_name
        if mission_file is None:
            self.mission_file=mission_name
        else:
            self.mission_file=mission_file
        self.debug=debug
        self.time_stamp=-1
        Global.MISSION_INSTANCE=self
    
    def start_mission(self,env_info):
        self.session=GlobalSettings.SESSION
        self.mission_info=Global.load_mission_info(self.mission_file)
        self.agent_id_list=env_info.get("agent_list",self.mission_info.get("agent_list",[]))
        self.agents=[]
        
        for agent_id in self.agent_id_list:
            agent=MAgent(agent_id)
            self.agents.append(agent)
            
        self.log_debug(f">> Start Mission [{self.mission_name}]<<")
    
    def next_step(self,step_index):
        self.log_debug(f">> Run Mission [{self.mission_name}] step [{step_index}]<<")
        self.time_stamp=step_index
    
    def check_end_mission(self) -> bool:
        return False
    
    def finish_mission(self):
        self.log_debug(f">> Finish Mission [{self.mission_name}]<<")
         
    def log_debug(self,content):
        if self.debug:
            print(content)
        if GlobalSettings.DEBUG_MISSION_LOG:
            time=Global.get_now_time_in_YMD_HMS()
            log_file=f"{Global.get_storage_path(self.mission_name)}/debug_log.json"
            Global.write_to_file_append(log_file,f"[{time}] {content} \n")
            
            
    def log_record(self,content):
        print(content)
        if GlobalSettings.MISSION_RECORD_TO_FILE:
            time=Global.get_now_time_in_YMD_HMS()
            log_file=f"{Global.get_storage_path(self.mission_name)}/record.json"
            Global.write_to_file_append(log_file,f"[{time}] {content} \n")
            
    def get_time_stamp(self)->int:
        return self.time_stamp + 1000000
    
    
    def get_mission_content(self,agent_id)->str:
        return ""
    
    def get_mission_name(self)->str:
        return 'MissionBase'
    
    
    def get_format_result(self,response,pattern):
        content=response.get('content')
        return re.findall(pattern,content)
        