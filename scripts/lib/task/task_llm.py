from settings import GlobalSettings

import json 
import os, glob
import re 
from lib.chat_model.llm_chat_model import ChatModel
from lib.mglobal.global_function import Global
from lib.language.language_dict import LanguageDict
import time

class LLMTaskFunction:
    @staticmethod
    def get_keys_from_template(task_template) -> list[str]:
        """
        get input keys from task template 

        Args:
            template (string ): the full task template content 

        Returns:
            list of string: the parameter name of input in upper case 
        """
        if "<comment>###<comment>" in task_template:
            task_template = task_template.split("<comment>###<comment>")[1]

        input_pattern='!<INPUT (\w+)>!'
        matches=re.findall(input_pattern,task_template)
        matches=list(set(matches))
        return [x.upper() for x in matches]
    
    @staticmethod
    def get_task_template(task):
        task_template =  Global.load_task(task)
        if "<comment>###<comment>" in task_template:
            task_template = task_template.split("<comment>###<comment>")[1]
            
        return task_template
    
    @staticmethod
    def get_prompt(task,input):
        task_template=LLMTaskFunction.get_task_template(task)
        
        prompt=task_template
        
        for key,value in input.items():
            prompt=prompt.replace(f"!<INPUT {key.upper()}>!",str(value))
            
        return prompt.strip()
    
    @staticmethod
    def get_all_tasks():
        """
        return all avaliable tasks in task folder

        Returns:
            List[str]: the list of all task name in lower case 
        """
        task_path=GlobalSettings.TASK_PATH
        task_list=[]
        for file in os.listdir(task_path):
            if file.endswith('.txt'):
                task_list.append(file.strip('.txt'))
        return task_list
        
    @staticmethod
    def get_message_legacy(task,agent_id,input,system_key=None):
        prompt=LLMTaskFunction.get_prompt(task,input)
        agent_info=Global.load_agent_info(agent_id)
        
        if system_key == None:
            msg=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
            return msg
        else:
            system_prompt = agent_info.get(system_key) if system_key in agent_info else ""
            msg=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
            return msg
            
    @staticmethod
    def get_message(task,agent_desc,input):
        prompt=LLMTaskFunction.get_prompt(task,input)
        
        if agent_desc == None:
            msg=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
            return msg
        else:
            msg=[
                {
                    "role":"system",
                    "content":agent_desc
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
            return msg
        
        
    @staticmethod
    def get_parm(agent_id,system_key='None'):
        agent_info=Global.load_agent_info(agent_id)
        if system_key is None:
            system_key='None'
        system_param_key=system_key+"_param"
        param={}
        if system_param_key in agent_info:
            info=agent_info[system_param_key]
        else:
            info=agent_info
            
        if 'temperature' in info:
            param['temperature']=info['temperature']
        if 'presence_penalty' in info:
            param['presence_penalty']=info['presence_penalty']
        if 'frequency_penalty' in info:
            param['frequency_penalty']=info['frequency_penalty']
            
        return param
        
        
    @staticmethod
    def get_llm_model_for_task(task):
        return GlobalSettings.LLM_MODEL
        # llm_type=GlobalSettings.LLM_TASK_DICT[task] if task in GlobalSettings.LLM_TASK_DICT else 'default'
        # return GlobalSettings.LLM_MODEL_DICT[llm_type]
        
    @staticmethod
    def log_debug(task,agent_name,data):
        time=Global.get_now_time_in_YMD_HMS()
        time=time.replace(":","=")
        debug_log_path=f"{Global.get_storage_path(agent_name)}/debug/log_{agent_name}_{task}_{time}.json"
        Global.json_save(debug_log_path,data)
        
    @staticmethod
    def log_debug_path(task,root_path,data):
        time=Global.get_now_time_in_YMD_HMS()
        time=time.replace(":","=")
        debug_log_path=f"{root_path}/debug/log_{task}_{time}.json"
        Global.json_save(debug_log_path,data)
        
    @staticmethod
    def call_model_legacy(task,agent_id,input,agent_ref_key,debug=False):
        message=LLMTaskFunction.get_message_legacy(task,agent_id,input,agent_ref_key)
        param=LLMTaskFunction.get_parm(agent_id,agent_ref_key)
        llm_model=LLMTaskFunction.get_llm_model_for_task(task)
        
        model=ChatModel(model=llm_model,debug=debug)
        response=model.send(message,param)
        
        if GlobalSettings.DEBUG_LOG_LLM_MESSAGE:
            debug_data={'message':message,'param':param,'model':llm_model,'response':response,'time':Global.get_now_time_in_YMD_HMS()}
            LLMTaskFunction.log_debug(task,agent_id,debug_data)
            
        return response
    
    @staticmethod
    def call_model(task,agent_id,agent_desc,input,agent_ref_key=None,debug=False):
        message=LLMTaskFunction.get_message(task,agent_desc,input)
        param=LLMTaskFunction.get_parm(agent_id,agent_ref_key)
        llm_model=LLMTaskFunction.get_llm_model_for_task(task)
        
        model=ChatModel(model=llm_model,debug=debug)
        response=model.send(message,param)
        
        if GlobalSettings.DEBUG_LOG_LLM_MESSAGE:
            debug_data={'message':message,'param':param,'model':llm_model,'response':response,'time':Global.get_now_time_in_YMD_HMS()}
            LLMTaskFunction.log_debug(task,agent_id,debug_data)
            
        return response
    
    @staticmethod
    def log_task_debug(content,debug=False):
        if debug:
            print(content)
    
    @staticmethod
    def standard_agent_llm_call(task,input,agent_obj,mission,agent_desc_key='default',use_system_call=False,fake_content=None):
        agent_id=agent_obj.get_id()
        debug=task in GlobalSettings.DEBUG_TASK
        if use_system_call:
            agent_desc=None
        else:
            agent_desc=agent_obj.description.get(agent_desc_key,agent_obj.description.get('default'))
        
        LLMTaskFunction.log_task_debug(f">> [{task}] Input : >>",debug)
        LLMTaskFunction.log_task_debug(input,debug)
        
        start_time=time.time()
        
        if fake_content != None:
            response={
                'content':fake_content
            }
        else:
            response=LLMTaskFunction.call_model(task=task,
                                            agent_id=agent_id,
                                            agent_desc=agent_desc,
                                            input=input,
                                            debug=debug)
        
        end_time=time.time()
        duration=end_time-start_time
        
        LLMTaskFunction.log_task_debug(f">> [{task}] Response : >>",debug)
        LLMTaskFunction.log_task_debug(response,debug)
        
        response['time_use']=duration
        response['agent_id']=agent_obj.get_id()
        response['task']=task
        response['mission']=mission.get_mission_name()
        return response
            
            
    @staticmethod
    def analyze_llm_call(task,input,agent_desc=None,debug=False,path=None):        
        
        start_time=time.time()
        
        message=LLMTaskFunction.get_message(task,agent_desc,input)
        param={"temperature":1.0}
        llm_model=LLMTaskFunction.get_llm_model_for_task(task)
        
        model=ChatModel(model=llm_model,debug=debug)
        response=model.send(message,param)
        
        if GlobalSettings.DEBUG_LOG_LLM_MESSAGE and path != None:
            debug_data={'message':message,'param':param,'model':llm_model,'response':response,'time':Global.get_now_time_in_YMD_HMS()}
            LLMTaskFunction.log_debug_path(task,path,debug_data)
        
        end_time=time.time()
        duration=end_time-start_time
        
        response['time_use']=duration
        response['task']=task
        
        return response
        
            
    @staticmethod
    def get_agent_judgement(agent_obj,mission):
        agent_judgement=""
        if GlobalSettings.USE_MISSION_JUDGE:
            agent_judgement="Here are your judgement toward the other agents:\n"
            agent_judgement+="\n".join(mission.get_agent_judgement(agent_obj.get_id()))
        return agent_judgement
    
    @staticmethod
    def get_agent_favors(agent_obj,mission):
        agent_favors=""
        if GlobalSettings.USE_FAVOR:
            agent_favors=";".join(mission.get_agent_favor(agent_obj.get_id()))
            agent_favors=f"Your attitude toward other agents: \n {agent_favors}"
        return agent_favors
    
    @staticmethod
    def get_next_strategy(agent_obj,mission):
        next_strategy=""
        if GlobalSettings.USE_NEXT_STRATEGY:
            next_strategy=mission.get_next_strategy(agent_obj.get_id())
            next_strategy=f"You decide to do in the speech: \n {next_strategy}"
        return next_strategy
    
    @staticmethod 
    def generate_dialog(agent_obj,mission,agent_desc_key='default',ignore_memory=False):
        task='generate_dialog'
        agent_name=agent_obj.get_name()
        agents=";".join(mission.get_agents())
        agents=f"Here are the players in the game:\n{agents}"
        limit_word=GlobalSettings.TALK_WORD_LIMIT
        mission_content=mission.get_mission_content(agent_obj.get_id())
        agent_favors=LLMTaskFunction.get_agent_favors(agent_obj,mission)
        next_strategy=LLMTaskFunction.get_next_strategy(agent_obj,mission)
        remember_count=GlobalSettings.DIALOG_MEMORY_COUNT
        if ignore_memory:
            memory=""
        else:
            memory=agent_obj.find_most_relative_memory(type_list=['chat'],time_step_range=999,count=remember_count)
        
        input={
            'MISSION' : mission_content,
            'NAME' : agent_name,
            'AGENTS' : agents,
            'DIALOG_MEMORY':memory,
            'LIMIT_WORD':limit_word,
            'AGENT_FAVORS':agent_favors,
            'NEXT_STRATEGY':next_strategy,
        }
        
        fake_content=None
        if GlobalSettings.USE_FAKE_DIALOG:
            fake_content="Villager, my role is straightforward but challenging. I must help uncover the Werewolf while protecting the Seer and Mason."
        
        return LLMTaskFunction.standard_agent_llm_call(task=task,
                                                input=input,
                                                agent_obj=agent_obj,
                                                mission=mission,
                                                agent_desc_key=agent_desc_key,
                                                fake_content=fake_content)
        
    @staticmethod
    def get_mission_werewolf_judge(agent_obj,mission,agent_desc_key):
        task='mission_werewolf_judge'
        
        agent_name=agent_obj.get_name()
        mission_content=f"Your Mission is:\n{mission.get_mission_content(agent_obj.get_id())}"
        remember_count=GlobalSettings.JUDGE_MEMORY_COUNT
        memory=agent_obj.find_most_recent_memory(type='chat',time_step_range=remember_count,count=remember_count)
        memory=f"The previous dialog is:\n{memory}"
        agents=";".join(mission.get_agents())
        agent_favors=LLMTaskFunction.get_agent_favors(agent_obj,mission)
        roles=";".join(mission.get_role_types())
        
        input={
            'MISSION' : mission_content,
            'NAME' : agent_name,
            'DIALOG_MEMORY':memory,
            'AGENTS':agents,
            'AGENT_FAVORS':agent_favors,
            'ROLES':roles,
        }
        return LLMTaskFunction.standard_agent_llm_call(task=task,
                                                input=input,
                                                agent_obj=agent_obj,
                                                mission=mission,
                                                agent_desc_key=agent_desc_key)
    
    @staticmethod
    def generate_favor(agent_obj,mission,agent_desc_key):
        task="generate_favor"
        
        agent_name=agent_obj.get_name()
        remember_count=GlobalSettings.FAVOR_MEMORY_COUNT
        memory=agent_obj.find_most_recent_memory(type='chat',time_step_range=remember_count,count=remember_count)
        agents=";".join(mission.get_agents())
        agent_judgement=LLMTaskFunction.get_agent_judgement(agent_obj,mission)
        
        input={
            'NAME' : agent_name,
            'DIALOG_MEMORY':memory,
            'MISSION_JUDGEMENT':agent_judgement,
            'AGENTS':agents
        }
        
        fake_content=None
        if GlobalSettings.USE_FAKE_FAVOR:
            fake_content="<Alpha,7>\n<Beta,4>"
        
        return LLMTaskFunction.standard_agent_llm_call(task=task,
                                                input=input,
                                                agent_obj=agent_obj,
                                                mission=mission,
                                                agent_desc_key=agent_desc_key,
                                                fake_content=fake_content)
        
    @staticmethod
    def mission_decide_next_strategy(agent_obj,mission,agent_desc_key):
        task="mission_decide_next_strategy"
        
        agent_name=agent_obj.get_name()
        mission_content=mission.get_mission_content(agent_obj.get_id())
        agent_judgement=LLMTaskFunction.get_agent_judgement(agent_obj,mission)
        strategy_ref=mission.get_strategy_ref(agent_obj.get_id())
        
        input={
            'NAME' : agent_name,
            'MISSION':mission_content,
            'MISSION_JUDGEMENT':agent_judgement,
            'STRATEGY_REF':strategy_ref
        }
        return LLMTaskFunction.standard_agent_llm_call(task=task,
                                                input=input,
                                                agent_obj=agent_obj,
                                                mission=mission,
                                                agent_desc_key=agent_desc_key)
    
    
    @staticmethod
    def mission_werewolf_vote(agent_obj,mission,agent_desc_key):
        task="mission_werewolf_vote"
        
        agent_name=agent_obj.get_name()
        mission_content=mission.get_mission_content(agent_obj.get_id())
        strategy_ref=mission.get_strategy_ref(agent_obj.get_id())
        agent_favors=LLMTaskFunction.get_agent_favors(agent_obj,mission)
        remember_count=GlobalSettings.VOTE_MEMORY_COUNT
        agents=";".join(mission.get_agents())
        memory=agent_obj.find_most_recent_memory(type='chat',time_step_range=remember_count,count=remember_count)
        
        input={
            'NAME' : agent_name,
            'MISSION':mission_content,
            "DIALOG_MEMORY":memory,
            "AGENTS" : agents,
            "AGENT_FAVORS":agent_favors
        }
        return LLMTaskFunction.standard_agent_llm_call(task=task,
                                                input=input,
                                                agent_obj=agent_obj,
                                                mission=mission,
                                                agent_desc_key=agent_desc_key)
        
    @staticmethod
    def boardcast_chat(targets,sender_agent,content,importance_dict=None):
        sender_name=sender_agent.get_name()
        
        for agent in targets:
            agent_name=agent.get_name()
            lang=agent.get_lang()
            say=LanguageDict.translate('say',lang)
            importance=50.0
            if agent.get_id()==sender_agent.get_id(): # send by self
               importance=5.0
            else: 
                if importance_dict!=None:
                    importance=importance_dict.get(agent.get_name(),50.0)
            key_list=[sender_name,agent_name]
            agent.remember(type='chat',
                           sub=sender_name,
                           verb=say,
                           obj=content,
                           key_list=key_list,
                           importance=importance)
            
            
   
    
    @staticmethod
    def embedding(content,debug=False):
        model=ChatModel(debug=debug)
        response=model.get_embedding(content=content,debug=debug)
        return response
    
    @staticmethod 
    def analyze_evaluate(content,evaluate_task,path=None):
        
        agent_desc=None
        task=''
        if 'interest' in evaluate_task:
            task='analyze_evaluate_interest'
            agent_desc="You are an audience who enjoys fun. You give higher scores to content that is novel, humorous, cute, and interesting, and lower scores to content that is monotonous, repetitive, and similar."
        elif 'surprise' in evaluate_task:
            task='analyze_evaluate_surprise'
            agent_desc="You are a meticulous and attentive reader who carefully evaluates the reasonableness of the reading material. You would give higher scores to content that is within reason but unexpected, diverse, and with twists, and lower scores to content that is simple, repetitive, and predictable."
        elif 'attraction' in evaluate_task:
            task='analyze_evaluate_attraction'
            agent_desc="You are an audience who loves to have fun and enjoys the thrilling and exciting plot of the Werewolf game."
        elif 'mem' in evaluate_task:
            task='analyze_evaluate_memorize'
            agent_desc="You are a passionate reader who only remembers the most exciting parts of the text."
        elif 'variation' in evaluate_task:
            task='analyze_evaluate_variation'
            agent_desc="You are a careful reader, you will study the details in the conversation carefully."
       
        input={
            'DIALOGS' : content,
        }
        
        if task != '':
            return LLMTaskFunction.analyze_llm_call(task=task,
                                                    input=input,
                                                    agent_desc=agent_desc,
                                                    path=path)
        else:
            return {'error' : 'Cannot find the task'}