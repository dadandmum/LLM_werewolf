from lib.mission.mission_base import MissionBase
from lib.task.task_llm import LLMTaskFunction
from lib.language.language_dict import LanguageDict
from lib.mglobal.global_function import Global
from lib.analyze.analyze_recorder import AnalyzeRecorder
from settings import GlobalSettings
import random
import re 
import time 

class TrustInfo:
    """
    The turst infomration of one agent to another 
    all possible role will be consider in this info 
    """
    def __init__(self,self_agent,agent_obj,roles):
        self.self_agent=self_agent
        self.target_agent=agent_obj
        self.trust_dict=dict()
        for r in roles:
            self.trust_dict[r.lower()]=0
            
    def to_str(self):
        result=f"[{self.self_agent.get_name()}]-judge->[{self.target_agent.get_name()}]\n"
        for key,value in self.trust_dict.items():
            if value > 0:
                result+=f"  {key} : {value}   "
        result+="\n"
        return result
    
    def update(self,trust_score_list):
        for key in self.trust_dict.keys():
            self.trust_dict[key]=0
        
        for info in trust_score_list:
            target=info[0]
            role=info[1]
            score=float(info[2])
        
            if target.upper()==self.target_agent.get_name().upper():
                self.trust_dict[role]=score
                
    def to_judgement(self):
        judge_role="villager"
        judge_val=0
        for key,value in self.trust_dict.items():
            if value > judge_val:
                judge_val=value
                judge_role=key.lower()
        posibility=judge_val
        
        return (f"{self.target_agent.get_name()} has a {posibility*100}% chance to be a {judge_role}" , judge_role,posibility)
        
class WerewolfInfo:
    def __init__(self,agent_obj,self_role,other_agents,roles,team):
        self.self_agent=agent_obj
        self.self_role=self_role
        role_types=list(set(roles))
        self.team=team
        self.trust_list=[]
        self.favor_dict=dict()
        self.next_stratgy=""
        self.vote=""
        for agent in other_agents:
            if agent.get_id() != self.self_agent.get_id():
                info=TrustInfo(self.self_agent,agent,role_types)
                self.trust_list.append(info)
                self.favor_dict[agent.get_name()]=50
                
    def set_mission(self,mission):
        self.mission_main=mission[0]
        self.mission_personal=mission[1]
        
    def equals(self,other):
        return self.self_agent.get_id()==other.self_agent.get_id()
        
    def to_str(self):
        result=f"[WerewolfInfo({self.self_agent.get_id()})]:\n"
        result+=f">> [Name]:{self.self_agent.get_name()}\n"
        if GlobalSettings.UES_RANDOM_BIG_FIVE:
            result+=f">> [BFTrait]:{self.self_agent.bf_trait}\n"
        result+=f">> [Role]:{self.self_role}\n"
        result+=f">> [Mission]:{self.mission_personal}\n"
        if GlobalSettings.USE_NEXT_STRATEGY:
            result+=f">> [NextStrategy]:{self.next_stratgy}\n"
        if GlobalSettings.USE_MISSION_JUDGE:
            result+=">> [Judge]\n"
            for t in self.trust_list:
                result+=t.to_str()
        if GlobalSettings.USE_FAVOR:
            result+=">> [Favor]\n"
            for name,favor in self.favor_dict.items():
                result+=f"  {self.self_agent.get_name()}-love->{name} : {favor}\n"
            
        return result
    
    def get_mission(self):
        return f"{self.mission_main} \n{self.mission_personal}"
    
    
    def update_trust(self,trust_score_list):
        for i in range(len(self.trust_list)):
            self.trust_list[i].update(trust_score_list)
            
    
    def get_team_judgement(self,self_role,other_role):
        is_friend=False
        for roles in self.team:
            if self_role in roles and other_role in roles:
                is_friend=True
                break
            elif self_role in roles or other_role in roles:
                is_friend=False
                break
            
        if is_friend:
            return ', which is your teammate'
        else:
            return ', which is your opponent'
    
    def to_judgement(self):
        result=[]
        
        self_role=self.self_role
        for trust in self.trust_list:
            (desc,other_role,o_psb)=trust.to_judgement()
            desc+=self.get_team_judgement(self_role.lower(),other_role.lower())
            result.append(desc)
            
        return result
    
    def set_favor(self,favor_list):
        def clamp(x,x_min,x_max):
            return min(x_max,max(x_min,x))
        
        for favor in favor_list:
            name=favor[0]
            value=float(favor[1])
            self.favor_dict[name]=clamp(value,0,100)        
    
    def update_favor(self,favor_list):
        def clamp(x,x_min,x_max):
            return min(x_max,max(x_min,x))
        
        for favor in favor_list:
            name=favor[0]
            value=float(favor[1])
            value_add=((value-1)*10/9*2-10)*3
            
            if name in self.favor_dict:
                self.favor_dict[name]=clamp(self.favor_dict[name]+value_add,0,100)

    def to_favor(self):
        result=[]
        favor_distribution=[(20,'strongly loathe'),
                            (40,'fairly dislike'),
                            (60,'feel neutral toward '),
                            (80,'pretty much appreciate'),
                            (101,'strongly adore')]
        for name, favor in self.favor_dict.items():
            verb=Global.get_distribution_value(favor,favor_distribution,0)
            result.append(f'You {verb} {name}.')
        
        return result
    
    def get_favor(self,agent_obj):
        return self.favor_dict.get(agent_obj.get_name())
    
    def update_next_strategy(self,strategy):
        self.next_stratgy=strategy
        
    def get_next_strategy(self):
        return self.next_stratgy

    def update_vote(self,vote_for):
        self.vote=vote_for

class Werewolf(MissionBase):
    def __init__(self, mission_name, mission_file=None,debug=True):
        super(Werewolf,self).__init__(mission_name, mission_file,debug)
        
    def start_mission(self, env_info):
        super().start_mission(env_info)
        
        # setup index 
        self.talk_index=0
        self.player_count=len(self.agents)
        self.max_turn=int(self.mission_info.get('max_turn',2))
        self.log_record(f"[Werewolf][StartMission]>> Total player:{self.player_count} Total round:{self.max_turn}")
        
        # setup roles 
        # roles=env_info.get('roles',['werewolf','villager'])
        roles=self.mission_info.get('roles',[])
        if len(roles) != self.player_count:
            self.log_record(f"[Error] The player number ({self.player_count}) is not equals to the role number ({len(roles)}). ")
            roles=['villager']*self.player_count
        random.shuffle(roles)
        
        self.role_types=list(set(roles))
        
        role_desc=[f"[{x}]" for x in roles]
        roles_content="".join(role_desc)
        self.log_record(f"[Werewolf][StartMission]>> Roles: {roles_content}")
        
        # set up werewolf info for each agents 
        self.werewolf_info_list=[]
        role_index=0
        team=self.mission_info.get('team')
        for agent in self.agents:
            role=roles[role_index]
            werewolf_info=WerewolfInfo(agent_obj=agent
                              ,self_role=role
                              ,other_agents=self.agents
                              ,roles=roles
                              ,team=team)
            self.werewolf_info_list.append(werewolf_info)
            role_index+=1
            
        
        for info in self.werewolf_info_list:
            info.set_mission(self.get_mission(info,self.mission_info))
            
        self.log_record("[Werewolf][StartMission]>> Agent Status >>")
        for info in self.werewolf_info_list:
            self.log_record(info.to_str())
            
        # init analyze
        self.analyze=AnalyzeRecorder(self)
            
            
    def next_step_update_index(self,step_index):
        self.log_debug(f">> Run Mission [{self.mission_name}] step [{step_index}]<<")
        self.time_stamp=step_index
        self.talk_index=step_index%self.player_count
        self.round_index=step_index//self.player_count
        
    def next_step(self, step_index):
        self.next_step_update_index(step_index)
        
        talk_agent=self.agents[self.talk_index]
        time_dict=dict()
        
        agent_key='default'
        if GlobalSettings.UES_RANDOM_BIG_FIVE:
            agent_key='bigfive'
            
        if GlobalSettings.USE_FAVOR:
            response = self.do_generate_favor(talk_agent,agent_key)
            time_dict['favor']=response.get('time_use')
            
        if GlobalSettings.USE_MISSION_JUDGE:
            response = self.do_mission_judge(talk_agent,agent_key)
            time_dict['judge']=response.get('time_use')
        
        if GlobalSettings.USE_NEXT_STRATEGY:
            response = self.do_decide_next_strategy(talk_agent,agent_key)
            time_dict['next_strategy']=response.get('time_use')
            
        self.log_record(self.get_info(talk_agent.get_id()).to_str())
            
        dialog=self.do_generate_talk(talk_agent,self,agent_key)
        
        if GlobalSettings.USE_ANALYZE:
            self.log_record("** Start Analayze **")
            start_time=time.time()
            self.analyze.record_dialog(talk_agent,self.get_info(talk_agent.get_id()),dialog)
            self.analyze.record_time(talk_agent,time_dict)
            # self.analyze.record_judgement(talk_agent,self.get_info(talk_agent.get_id()))
            if GlobalSettings.USE_TURN_ANALYZE and self.talk_index == self.player_count - 1:
                self.log_record("** Start Vote ***")
                vote_dict=self.do_vote(agent_key)
                self.analyze.record_vote(vote_dict,self.round_index)
                self.log_record("[Vote Result]")
                self.log_record(vote_dict)
            end_time=time.time()
            self.log_record(f"** End Analayze({end_time-start_time}s) **")
        
        
        for agent in self.agents:
            agent.flush_memory()
            
        self.log_record("[Werewolf] - End Next Step - ")
        
    def check_end_mission(self) -> bool:
        return (self.round_index >= (self.max_turn-1)) and (self.talk_index >= (self.player_count - 1))
    
    def finish_mission(self):
        super().finish_mission()
        self.log_record("[Werewolf] - End Mission - ")
        
        if GlobalSettings.USE_ANALYZE:
            self.analyze.final_analyze()
    
    def get_mission_content(self, agent_id) -> str:
        info = self.get_info(agent_id)
        return info.get_mission()
    
    def get_mission_name(self) -> str:
        return 'Werewolf'
    
    ################### LOGIC ####################
    def get_info(self,agent_id):
        for info in self.werewolf_info_list:
            if info.self_agent.get_id()==agent_id:
                return info

    def get_info_index(self,agent_id):
        for i in range(len(self.werewolf_info_list)):
            if self.werewolf_info_list[i].self_agent.get_id()==agent_id:
                return i
        
    def get_info_by_name(self,agent_name):
        for i in range(len(self.werewolf_info_list)):
            if self.werewolf_info_list[i].self_agent.get_name()==agent_name:
                return self.werewolf_info_list[i]
            
    def get_mission(self,info,mission_info):
        role=info.self_role
        main=mission_info.get('main','')
        personal=mission_info.get('personal').get(role)
        
        if role == 'seer':
            others=[x for x in self.werewolf_info_list if not(x.equals(info)) ]
            # check=random.choice(others)
            # if check.self_role=="werewolf":
            #     role="a werewolf"
            # else:
            #     role="not a werewolf"
            # personal=personal.replace('<AGENT_NAME>',check.self_agent.get_name() ).replace('<ROLE>',role)
            check=random.sample(others,2)
            if check[0].self_role=="werewolf" or check[1].self_role=="werewolf":
                role="a werewolf"
            else:
                role="not a werewolf"
            personal=personal.replace('<AGENT_NAME>', f"{check[0].self_agent.get_name()} or {check[1].self_agent.get_name()}" ).replace('<ROLE>',role)
        elif role == 'werewolf':
            # minion=[x for x in self.werewolf_info_list if x.self_role=="minion"][0]
            # personal=personal.replace('<AGENT_NAME>',minion.self_agent.get_name() ).replace('<ROLE>',minion.self_role)
            pass 
        elif role == 'minion':
            # werewolf=[x for x in self.werewolf_info_list if x.self_role=="werewolf"][0]
            # personal=personal.replace('<AGENT_NAME>',werewolf.self_agent.get_name() ).replace('<ROLE>',werewolf.self_role)
            pass 
        elif role == 'witcher':
            others=[x for x in self.werewolf_info_list if not(x.equals(info)) ]
            minion=[x for x in self.werewolf_info_list if x.self_role=="minion"][0]
            others_without_minion=[x for x in others if not(x.equals(minion)) ]
            pick=random.choice(others_without_minion)
            two_player=[minion,pick]
            random.shuffle(two_player)
            personal=personal.replace('<AGENT_NAME>', f"either {two_player[0].self_agent.get_name()} or {two_player[1].self_agent.get_name()}" ).replace('<ROLE>','minion')
             
        elif role == 'mason':
            others=[x for x in self.werewolf_info_list if not(x.equals(info)) ]
            mason=[x for x in others if x.self_role=="mason"][0]
            personal=personal.replace('<AGENT_NAME>',mason.self_agent.get_name() ).replace('<ROLE>',mason.self_role)
            
            
        return (main,personal)
    
    def get_agents(self):
        return [x.get_name() for x in self.agents]
    
    def get_favor(self,agent_id):
        info=self.get_info(agent_id)
        return info.to_favor()
    
    def get_role_types(self):
        return self.role_types
    
    def generate_favor_dict_agents_to_target(self,agents,target):
        imp_dict=dict()
        
        for agent in agents:
            if target.get_id()!=agent.get_id():
                info = self.get_info(agent.get_id())
                favor=info.get_favor(target)
                if favor !=None:
                    imp_dict[agent.get_name()]=favor
            
        return imp_dict
    
    def generate_favor_dict_agent_to_others(self,agent,others):
        imp_dict=dict()
        
        info = self.get_info(agent.get_id())
        for other in others:
            if other.get_id()!=agent.get_id():
                favor=info.get_favor(other)
                if favor != None:
                    imp_dict[other.get_name()]=favor
            
        return imp_dict
    
    
    def do_generate_talk(self,agent_obj,mission,agent_key):
        self.log_record("** Start Generate Talk **")
        
        favor_dict=self.generate_favor_dict_agent_to_others(agent_obj,self.agents)
        agent_obj.update_chat_favor(favor_dict)
        
        response=LLMTaskFunction.generate_dialog(agent_obj=agent_obj,
                                                 mission=mission,
                                                 agent_desc_key=agent_key)
        time_use=response.get('time_use')
        self.log_record(f"** End Generate Talk (Time use:{time_use}s) **")
        
        # result=LLMTaskFunction.generate_dialog(talk_agent,self,agent_key)
        dialog=Global.clean_dialog_content(response.get('content',''),agent_obj.get_name())
        
        self.log_record(f"[Werewolf] (dialog({self.round_index},{self.talk_index})) \n {agent_obj.get_name()} says: {dialog}\n")
        
        
        favor_dict_att=self.generate_favor_dict_agents_to_target(self.agents,agent_obj)
        LLMTaskFunction.boardcast_chat(self.agents,
                                       agent_obj,
                                       dialog,
                                       favor_dict_att)
        
            
        return dialog
    
    def do_mission_judge(self,agent_obj,agent_key):
        self.log_record("** Start Mission Judge **")
        agent_id=agent_obj.get_id()
        response=LLMTaskFunction.get_mission_werewolf_judge(agent_obj=agent_obj,mission=self,agent_desc_key=agent_key)
        
        # get result list 
        pattern="<(\w+),(\w+),([0-9.]+)>"
        content=response.get('content').replace(' ','')
        time_use=response.get('time_use')
        trust_score_list=re.findall(pattern,content)
        
        self.werewolf_info_list[self.get_info_index(agent_id)].update_trust(trust_score_list)
        self.log_record(f"** End Mission Judge (Time use:{time_use}s) **")
        
        return response
        
    def get_agent_judgement(self,agent_id):
        info=self.get_info(agent_id)
        return info.to_judgement()
        
    def do_generate_favor(self,agent_obj,agent_key):
        self.log_record("** Start Generate Favor **")
        start_time=time.time()
        agent_id=agent_obj.get_id()
        response=LLMTaskFunction.generate_favor(agent_obj=agent_obj,
                                                mission=self,
                                                agent_desc_key=agent_key)
        
        # get result list 
        pattern="<(\w+),([0-9.]+)>"
        content=response.get('content').replace(' ','')
        favor_list=re.findall(pattern,content)
        
        self.werewolf_info_list[self.get_info_index(agent_id)].update_favor(favor_list)
        
        end_time=time.time()
        self.log_record(f"** End Generate Favor (Time use:{end_time-start_time}s) **")
        
        return response
        
    def get_agent_favor(self,agent_id):
        info=self.get_info(agent_id)
        return info.to_favor()
    
    def get_strategy_ref(self,agent_id):
        info=self.get_info(agent_id)
        role=info.self_role
        return self.mission_info.get('strategy',{}).get(role)
    
    def do_decide_next_strategy(self,agent_obj,agent_key):
        self.log_record("** Start Decide Next **")
        start_time=time.time()
        
        agent_id=agent_obj.get_id()
        response=LLMTaskFunction.mission_decide_next_strategy(agent_obj=agent_obj,mission=self,agent_desc_key=agent_key)
        
        strategy=response.get('content')
        self.werewolf_info_list[self.get_info_index(agent_id)].update_next_strategy(strategy)
        
        end_time=time.time()
        self.log_record(f"** End Decide Next (Time use:{end_time-start_time}s) **")
        return response
    
    def get_next_strategy(self,agent_id):
        info=self.get_info(agent_id)
        return info.get_next_strategy()
        
    def do_vote(self,agent_key):
        vote_dict=dict()
        for agent in self.agents:
            response=LLMTaskFunction.mission_werewolf_vote(agent_obj=agent,
                                                           mission=self,
                                                           agent_desc_key=agent_key)
            
            
            pattern="<(\w+)>"
            content=response.get('content').replace(' ','')
            
            vote_list=re.findall(pattern,content)
            agent_id=agent.get_id()
            if ( len(vote_list) > 0 ):
                vote=vote_list[0]
                info=self.get_info_by_name(vote)
                self_info=self.get_info_by_name(agent.get_name())
                if not(info is None):
                    vote_dict[agent_id]={'id':info.self_agent.get_id(),'name':info.self_agent.get_name(),'role':info.self_role , 'voter_role':self_info.self_role}
                self.werewolf_info_list[self.get_info_index(agent_id)].update_vote(vote)
            else:
                self.werewolf_info_list[self.get_info_index(agent_id)].update_vote("")
        return vote_dict