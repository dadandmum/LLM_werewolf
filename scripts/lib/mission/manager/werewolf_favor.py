
from lib.mglobal.global_function import Global
from lib.task.task_llm import LLMTaskFunction
from .werewolf import Werewolf
from settings import GlobalSettings
import random , re 


class WerewolfFavor(Werewolf):
    def __init__(self,mission_name,mission_file=None,debug=True):
        super(WerewolfFavor,self).__init__(mission_name,mission_file,debug)
        
    def get_agents(self):
        return [x for x in self.agent_names]
    
    def start_mission(self, env_info):
        super().start_mission(env_info)
        
        # set up fake history dialogs
        his_dialog=self.mission_info.get('history_dialog')
        his_agent=self.mission_info.get('history_dialog_sender')
        self.agent_names=list(set(his_agent))
        
        say='say'
        assert(len(his_dialog)==len(his_agent))
        for i in range(len(his_dialog)):
            dialog=his_dialog[i]
            speaker_name=his_agent[i]
            key_list=[speaker_name]
            for agent in self.agents:
                agent.remember(type='chat',
                               sub=speaker_name,
                               verb=say,
                               obj=dialog,
                               key_list=key_list,
                               importance=50
                               )
                
        if GlobalSettings.USE_FAVOR:
            # set up random favor
            favor_all=dict()
            for agent in self.agents:
                rand_favor=[]
                for hagent in self.agent_names:
                    rand_favor.append([hagent,random.randint(1,100)])
                
                self.werewolf_info_list[self.get_info_index(agent.get_id())].set_favor(rand_favor)
                favor_all[agent.get_id()]=rand_favor

            self.analyze.record_favor(favor_all)
            
            self.log_record("[WerewolfFavor] favor list ")
            self.log_record(favor_all)
        
        
    def next_step(self, step_index):
        self.next_step_update_index(step_index)
        
        agent_key='default'
        
        self.shuffle_memory()
        vote_dict=self.do_single_vote(agent_key)
        self.analyze.record_vote(vote_dict,step_index)
        
        self.log_record("[Vote Result]")
        self.log_record(vote_dict)
        
        
    def finish_mission(self):
        self.log_record("[WerewolfFavor] - End Mission - ")
        
    def shuffle_memory(self):
        for agent in self.agents:
            random.shuffle(agent.memory.events['chat'])
            # for i in range(len(agent.memory.events['chat'])):
            #     agent.memory.events['chat'][i].set_importance(random.random()*100)
        
    def do_single_vote(self,agent_key):
        vote_dict=dict()
        for agent in self.agents:
            
            
            response=LLMTaskFunction.mission_werewolf_vote(agent_obj=agent,
                                                           mission=self,
                                                           agent_desc_key=agent_key)
        
            pattern="<(\w+)>"
            content=response.get('content').replace(' ','')
            
            vote_list=re.findall(pattern,content)
            if ( len(vote_list) > 0 ):
                vote=vote_list[0]
            
                vote_dict[agent.get_id()]={'id':agent.get_id(),'name':vote , 'role':'villager','voter_role':'villager'}
                
        return vote_dict
        