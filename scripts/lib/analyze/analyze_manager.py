from settings import GlobalSettings
from lib.mglobal.global_function import Global
from .analyze_recorder import AnalyzeRecorder
import os , re 
from lib.task.task_llm import LLMTaskFunction
import numpy as np
# from sentence_transformers import SentenceTransformer
# from sentence_transformers.util import cos_sim

class AnalyzeManager:
    
    @staticmethod
    def get_record_list(session,record_key,folder='none')->list:
        if folder != 'none':
            session=f"{folder}/{session}"
        file_root=f"{GlobalSettings.STORAGE_PATH}/{session}/analyze"
        record_file=f"{file_root}/{record_key}.json"
        
        record=Global.json_load(record_file).get('record')
        
        return record
    
    @staticmethod
    def get_analyze_data(session,file_name,folder='none')->list:
        if folder != 'none':
            session=f"{folder}/{session}"
        file_root=f"{GlobalSettings.STORAGE_PATH}/{session}/analyze"
        record_file=f"{file_root}/{file_name}.json"
        
        data=Global.json_load(record_file)
        
        return data
    
    @staticmethod
    def get_embedding_dialog_record(session,folder='none',model=''):
        session_fix=session
        if folder != 'none':
            session_fix=f"{folder}/{session}"
        file_root=f"{GlobalSettings.STORAGE_PATH}/{session_fix}/analyze"
        
        if model == '' or model == 'default':
            embedding_key='embedding_tag'
        else:
            t_model=model.split('/')[-1]
            embedding_key=f'embedding_tag_{t_model}'
        
        # dialog_file=f"{file_root}/dialog.json"
        # record=Global.json_load(dialog_file).get('record')
        dialog_record=AnalyzeManager.get_record_list(session=session,record_key='dialog',folder=folder)
        
        for i in range(len(dialog_record)):
            embedding_tag=dialog_record[i][embedding_key]
            embedding_file=f"{file_root}/embedding/{embedding_tag}.json"
            embedding=Global.json_load(embedding_file).get('data')
            dialog_record[i]['embedding']=embedding
            
        return (file_root, dialog_record)
    
    @staticmethod
    def analyze_embedding_dialog(session,folder='none',model='',isPrint=True):
        # session_fix=session
        # if folder != 'none':
        #     session_fix=f"{folder}/{session}"
        # file_root=f"{GlobalSettings.STORAGE_PATH}/{session_fix}/analyze"
        
        # if model == '' or model == 'default':
        #     embedding_key='embedding_tag'
        # else:
        #     t_model=model.split('/')[-1]
        #     embedding_key=f'embedding_tag_{t_model}'
        
        # # dialog_file=f"{file_root}/dialog.json"
        # # record=Global.json_load(dialog_file).get('record')
        # dialog_record=AnalyzeManager.get_record_list(session=session,record_key='dialog',folder=folder)
        
        # for i in range(len(dialog_record)):
        #     embedding_tag=dialog_record[i][embedding_key]
        #     embedding_file=f"{file_root}/embedding/{embedding_tag}.json"
        #     embedding=Global.json_load(embedding_file).get('data')
        #     dialog_record[i]['embedding']=embedding
        
        (file_root,dialog_record)=AnalyzeManager.get_embedding_dialog_record(session=session,
                                                                             folder=folder,
                                                                             model=model)
            
        output=f"{file_root}/dialog_embedding.json"
        result=AnalyzeRecorder.final_analyze_dialog(dialog_record,output)
        
        for overall in result['overall']:
            step=overall.get('step')
            mean=overall.get('result').get('mean')
            std=overall.get('result').get('std')
            var=overall.get('result').get('var')
            if isPrint:
                print(f"{step:.3f}: {mean:.3f}|{std:.3f}")
        
        return result
        
    @staticmethod
    def analyze_embedding_dialog_by_agent(session='none',folder='temp',model='',isPrint=True):
        
        if session=='none':
            folder_root=f"{GlobalSettings.STORAGE_PATH}/{folder}"
            all_sessions=os.listdir(folder_root)
            session=all_sessions[0]
            print(f"run session {session}...")
            
        (file_root,dialog_record)=AnalyzeManager.get_embedding_dialog_record(session=session,
                                                                             folder=folder,
                                                                             model=model)
            
        output=f"{file_root}/dialog_embedding_by_agent.json"
        result=AnalyzeRecorder.analyze_dialog_by_agent(dialog_record,output)
        
        for agent,agent_result in result['agents'].items():
            mean=agent_result.get('mean')
            std=agent_result.get('std')
            var=agent_result.get('var')
            if isPrint:
                print(f"{agent}: {mean}|{std}")
                
        # output dialog content by agent
        for agent in result['agents'].keys():
            dialog_list=[x['dialog'] for x in dialog_record if x['sender_id']==agent]
            agent_dialog='\n'.join(dialog_list)
            output_file=f"{file_root}/agent_{agent}_dialog.txt"
            Global.file_save(output_file,agent_dialog)
        
        return result
        
        
    @staticmethod
    def clean_evalution(folder,analyze_type):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            
            evaluation_output_list=['evaluate_attraction','evaluate_interest','evaluate_mem','evaluate_surprise','evaluate_variation']
            ref_type=['att','int','mem','sur','var']
            
            for i in range(len(evaluation_output_list)):
                eof=evaluation_output_list[i]
                rt=ref_type[i]
                if rt in analyze_type or analyze_type=="*":
                    file=f"{GlobalSettings.STORAGE_PATH}/{folder}/{session_folder}/analyze/{eof}.json"
                    if Global.file_remove(file):
                        print(f"Remove File: {file}")
                
            

    @staticmethod
    def get_all_sessions(folder):
        folder_root=f"{GlobalSettings.STORAGE_PATH}/{folder}"
        list_dir=os.listdir(folder_root)
        all_sessions=[]
        for item in list_dir:
            path=os.path.join(folder_root,item)
            if os.path.isdir(path):
                all_sessions.append(item)
        
        def filter_session(inSession):
            pattern="([a-z_]+)"
            find=re.findall(pattern,inSession)
            env=find[0].strip("_")
            return (env,inSession)
        
        return [filter_session(x) for x in all_sessions]
        
    @staticmethod
    def analyze_embedding_folder(folder,model=''):
        # folder_root=f"{GlobalSettings.STORAGE_PATH}/{folder}"
        # all_sessions=os.listdir(folder_root)
        # all_sessions=[ x for x in all_sessions if not(x.endswith('.json'))]
        
        # def filter_session(inSession):
        #     pattern="([a-z_]+)"
        #     find=re.findall(pattern,inSession)
        #     env=find[0].strip("_")
        #     return (env,inSession)
        
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        folder_result=dict()
        
        output_file=f"{GlobalSettings.STORAGE_PATH}/{folder}/analyze_embedding.json"
        
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            # print(f"Now Analyze {session_folder}")
            result=AnalyzeManager.analyze_embedding_dialog(session=session_folder,folder=folder,model=model,isPrint=False)
            if session_type in folder_result:
                folder_result[session_type].append(result)
            else:
                folder_result[session_type]=[result]
        
        folder_item=dict()
        for key,list in folder_result.items():
            print(f"Key :{key}")
            key_item=dict()
            for result in list:
                for item in result.get('overall',[]):
                    step=item.get('step')
                    mean=item.get('result').get('mean')
                    std=item.get('result').get('std')
                    var=item.get('result').get('var')
                    # print(f">> {step}: {mean}|{std}|{var}")
                    if step in key_item:
                        key_item[step]['mean'].append(mean)
                        key_item[step]['std'].append(mean)
                        key_item[step]['var'].append(mean)
                    else:
                        key_item[step]={
                            'mean':[mean],
                            'std':[std],
                            'var':[var]
                        }
                        
            for k in key_item.keys():
                key_item[k]['mean_m']=sum(key_item[k]['mean'])/len(key_item[k]['mean'])
                key_item[k]['std_m']=sum(key_item[k]['std'])/len(key_item[k]['std'])
                key_item[k]['var_m']=sum(key_item[k]['var'])/len(key_item[k]['var'])
                print(f"! {k}!=> mean:{key_item[k]['mean_m']:.3f}, std: {key_item[k]['std_m']:.3f}, var: {key_item[k]['var_m']:.3f}" )
                
            folder_item[key]=key_item
            
        folder_result['overall']=folder_item
            
        Global.json_save(output_file,folder_result)

        
    @staticmethod
    def generate_embedding_from_content(content,model):
        
        if model.startswith('gte'):
            model=f"thenlper/{model}"
        stmodel = SentenceTransformer(model)
        result = stmodel.encode(content)
        return result.tolist()
        
    @staticmethod
    def generate_embedding_session(session,model,folder='none'):
        import time
        print(f"start generate embedding in session {session}")
        start_time=time.time()
        _session=session
        if folder != 'none':
            _session=f"{folder}/{session}"
        file_root=f"{GlobalSettings.STORAGE_PATH}/{_session}/analyze"
        dialog_file=f"{file_root}/dialog.json"
        
        record_list=AnalyzeManager.get_record_list(session=session,record_key='dialog',folder=folder)
        t_model=model.split('/')[-1]
        
        for i in range(len(record_list)):
            dialog=record_list[i].get('dialog')
            id=record_list[i].get('sender_id')
            ts=record_list[i].get('time_stamp')
            embedding=AnalyzeManager.generate_embedding_from_content(dialog,model)
            embedding_tag=f'{id}-{ts}-dialog-{t_model}'
            embedding_key=f'embedding_tag_{t_model}'
            embedding_path=f"{file_root}/embedding/{embedding_tag}.json"
            Global.json_save(embedding_path,{'data':embedding})
            print(f"   generate embedding for {id} , in time {ts}, length is {len(embedding)}")
            record_list[i][embedding_key]=embedding_tag
        
        Global.json_update(dialog_file,{'record':record_list})
        
        end_time=time.time()
        print(f" ** Finished. Time used :{end_time-start_time}s")
        
        
    
    @staticmethod
    def generate_embedding(folder,model):
        # folder_root=f"{GlobalSettings.STORAGE_PATH}/{folder}"
        # all_sessions=os.listdir(folder_root) 
        
        # def filter_session(inSession):
        #     pattern="([a-z_]+)"
        #     find=re.findall(pattern,inSession)
        #     env=find[0].strip("_")
        #     return (env,inSession)
        
        # f_sessions= [filter_session(x) for x in all_sessions ]
        
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        for session in f_sessions:
            AnalyzeManager.generate_embedding_session(session=session[1],
                                                      model=model,
                                                      folder=folder)
            

    @staticmethod
    def generate_LLM_evaluate_interest(output_root,dialog_content,session):
        response=LLMTaskFunction.analyze_evaluate(dialog_content,'interest',output_root)
        output_file=f"{output_root}/evaluate_interest.json"
        
        # pattern="<(\w+),([0-9.]+)>"
        # content=response.get('content').replace(' ','')
        # time_use=response.get('time_use')
        # score_list=re.findall(pattern,content)
        
        # result={'data':[]}
        # score_all=0
        # for item in score_list:
        #     name=item[0]
        #     score=float(item[1])
        #     result['data'].append({'name':name,'score':score})
        #     score_all+=score
            
        # ave_score=score_all/len(score_list)
        # result['value']=ave_score
        
        pattern="<([0-9.]+)>"
        content=response.get('content').replace(' ','')
        time_use=response.get('time_use')
        score_list=re.findall(pattern,content)
        if len(score_list) > 0:
            score=score_list[-1]
            result={'value':score}
            
            Global.json_add_item_to_list(output_file,'result',result)
        # print(result)
        
        print(f"** Finish Interest [{session}](Time use:{time_use}s) **")
            

    @staticmethod
    def generate_LLM_evaluate_surprise(output_root,dialog_content,session):
        response=LLMTaskFunction.analyze_evaluate(dialog_content,'surprise',output_root)
        output_file=f"{output_root}/evaluate_surprise.json"
        
        pattern="<([0-9.]+)>"
        content=response.get('content').replace(' ','')
        time_use=response.get('time_use')
        score_list=re.findall(pattern,content)
        
        score=score_list[-1]
        result={'value':score}
            
        Global.json_add_item_to_list(output_file,'result',result)
        # print(result)
        
        print(f"** Finish Surprise [{session}] (Time use:{time_use}s) **")
        
     
    @staticmethod
    def generate_LLM_evaluate_attraction(output_root,dialog_content,session):
        response=LLMTaskFunction.analyze_evaluate(dialog_content,'attraction',output_root)
        output_file=f"{output_root}/evaluate_attraction.json"
        
        # pattern="<(([0-9a-zA-Z.]+)+),([0-9.]+)>"
        pattern="<([0-9.]+)>"
        content=response.get('content').replace(' ','')
        time_use=response.get('time_use')
        score_list=re.findall(pattern,content)
        
        score=score_list[-1]
        result={'value':score}
        # score_all=0
        # for item in score_list:
        #     turn=item[0]
        #     score=float(item[1])
        #     result['result'].append({'turn':turn,'score':score})
        #     score_all+=score
            
        Global.json_add_item_to_list(output_file,'result',result)
        # print(result)
        
        print(f"** Finish Attraction  [{session}] (Time use:{time_use}s) **")
        
          
    @staticmethod
    def generate_LLM_evaluate_memorize(output_root,dialog_content,session):
        response=LLMTaskFunction.analyze_evaluate(dialog_content,'mem',output_root)
        output_file=f"{output_root}/evaluate_mem.json"
        
        pattern="<[ ]*'(.+)'[ ]*,[ ]*(\w+)[ ]*,[ ]*([0-9.]+)[ ]*>"
        content=response.get('content')
        time_use=response.get('time_use')
        score_list=re.findall(pattern,content)
        
        if len(score_list) > 0 :
            result={'data':[]}
            role_count={}
            role_expect={}
            score_all=0
            for item in score_list:
                word=item[0]
                role=item[1]
                score=float(item[2])
                result['data'].append({'word':word,'role':role,'score':score})
                score_all+=score
                if role in role_count:
                    role_count[role]=role_count[role]+1
                else:
                    role_count[role]=1
                if role in role_expect:
                    role_expect[role]=role_expect[role]+score
                else:
                    role_expect[role]=score
                
            ave_score=score_all/len(score_list)
            result['average']=ave_score
            result['role']=role_count
            result['role_expect']=role_expect
            
            Global.json_add_item_to_list(output_file,'result',result)
            # print(result)
        
        print(f"** Finish Memorize [{session}] (Time use:{time_use}s) **")
         
    @staticmethod
    def generate_LLM_evaluate_variation(output_root,dialog_record,session):
        
        turn=GlobalSettings.TALK_TURN
        agnet_count=int(len(dialog_record)/turn)
        time_use_all=0
        name_ref_dict=dict()
        
        for i in range(len(dialog_record)):
            record=dialog_record[i]
            sender_id=record.get('sender_id').lower()
            sender_role=record.get('sender_role').lower()
            if not(sender_id in name_ref_dict):
                name_ref_dict[sender_id]=sender_role
        names=list(name_ref_dict.keys())
            
    
        result_list=[]
        for t_index in range(turn):
            dialog_content=""
            for i in range(agnet_count):
                record=dialog_record[t_index*turn+i]
                name=record.get('sender_name')
                dialog=record.get('dialog')
                # personal=record.get('sender_personal')
                # personal=personal.split('.')[0].replace('You',name).replace('are','is')
                dialog_content+=f"{name} says: '{dialog}'\n"
                    
            response=LLMTaskFunction.analyze_evaluate(dialog_content,'variation',output_root)
            
            result=dict()
            for s in names:
                result[s]=dict()
                for t in names:
                    if s == t:
                        result[s][t]=name_ref_dict[s]
                    else:
                        result[s][t]='none'
            
            pattern="<[ ]*(\w+)[ ]*,[ ]*(\w+)[ ]*,[ ]*(\w+)[ ]*>"
            content=response.get('content')
            content_split=content.split('```')
            if len(content_split) > 1:
                content=content_split[1]
            var_list=re.findall(pattern,content)
            count=len(var_list)
            if count > 10:
                var_list=var_list[:10]
            
            for item in var_list:
                speaker=item[0].lower()
                target=item[1].lower()
                target_role=item[2].lower()
                if speaker in names and target in names:
                    result[speaker][target]=target_role
            time_use=float(response.get('time_use'))
            time_use_all+=time_use
            result_list.append({'turn':t_index,'result':result})
            
            print(f"** Variation Turn{t_index} (Time use:{time_use}s) **")
        
        output_file=f"{output_root}/evaluate_variation.json"
        
        final_json={'result_list':result_list}
        Global.json_add_item_to_list(output_file,'result',final_json)
        
        print(f"** Finish Variation [{session}] (Time use:{time_use_all}s) **")
         

    @staticmethod
    def generate_LLM_evaluate_session(folder,session,analyze_type="*"):
        
        print(f">>>>>>> Start Evaluate {folder} / {session} <<<<<<<<<")
        dialog_record=AnalyzeManager.get_record_list(session=session,record_key='dialog',folder=folder)
        output_root=f"{GlobalSettings.STORAGE_PATH}/{folder}/{session}/analyze"
        output_file=f"{output_root}/evaluate.json"
    
        dialog_content=""
        for record in dialog_record:
            name=record.get('sender_name')
            dialog=record.get('dialog')
            personal=record.get('sender_personal')
            personal=personal.split('.')[0].replace('You',name).replace('are','is')
            dialog_content+=f"{name}({personal}) says: '{dialog}'\n"
        
        if analyze_type=="*" or 'int' in analyze_type:
            AnalyzeManager.generate_LLM_evaluate_interest(output_root=output_root,dialog_content=dialog_content,session=session)
        if analyze_type=="*" or 'sur' in analyze_type:
            AnalyzeManager.generate_LLM_evaluate_surprise(output_root=output_root,dialog_content=dialog_content,session=session)
        if analyze_type=="*" or 'att' in analyze_type:
            AnalyzeManager.generate_LLM_evaluate_attraction(output_root=output_root,dialog_content=dialog_content,session=session)
        if analyze_type=="*" or 'mem' in analyze_type:
            AnalyzeManager.generate_LLM_evaluate_memorize(output_root=output_root,dialog_content=dialog_content,session=session)
        if analyze_type=="*" or 'var' in analyze_type:
            AnalyzeManager.generate_LLM_evaluate_variation(output_root=output_root,dialog_record=dialog_record,session=session)
            
    @staticmethod
    def generate_LLM_evaulate(folder,analyze_type):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        for session in f_sessions:
            AnalyzeManager.generate_LLM_evaluate_session(folder=folder,
                                                         session=session[1],
                                                         analyze_type=analyze_type)
            
            
    @staticmethod
    def simple_analyze_vote(folder):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        output_file=f"{GlobalSettings.STORAGE_PATH}/{folder}/analyze_vote.json"
        
        print(f_sessions)
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            
            vote_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='vote',folder=folder)
            
            favor_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='favor',folder=folder)
            favor_data=favor_data['record'][0]['favor']
            
            senders=list(favor_data.keys())
            targets=[]
            
            result=dict()
            for key in senders:
                data=favor_data[key]
                for item in data:
                    name = item[0]
                    if not name in targets:
                        targets.append(name)
            
            targets.sort()
            
            for sender_name in senders:
                result[sender_name]=dict()
                data=favor_data[sender_name]
                for item in data:
                    name = item[0]
                    favor_score = item[1]
                    result[sender_name][name]={"favor":favor_score,"vote":0}
            
            vote_data=vote_data['record']
            for data in vote_data:
                data=data['vote']
                for key,data in data.items():
                    sender_name=key
                    name = data['name']
                    if sender_name in result:
                        if name in result[sender_name]:
                            result[sender_name][name]["vote"] += 1
            
            
            print(f"[{session_folder}]>>>>>>>>>>>")
            print(result)
        
    @staticmethod
    def analyze_vote(folder):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        output_file=f"{GlobalSettings.STORAGE_PATH}/{folder}/analyze_vote.json"
        
        vote_result={}
        turn_record={}
        all_role=['villager','tanner','seer','mason','minion','werewolf']
        role_norm={'villager':0.5,'mason':0.5,'tanner':1.0,'seer':0.5,'minion':1.0,'werewolf':1.0}
        
        def add_to_dict(dict,key,count):
            if key in dict:
                dict[key]=dict[key]+count
            else:
                dict[key]=count
                
        def norm(result):
            sumall=sum(result.values())
            for role in role_norm.keys():
                if not(role in result):
                    result[role]=0
                else:
                    result[role]=result[role]/sumall*role_norm[role]
                    
                if role=='villager' or role=='mason':
                    result[role+"_"]=result[role]
            
                    
            data=np.array(list(result.values()))
            std=data.std()
            var=data.var()
            result['std']=std
            result['var']=var
            return result
        
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            
            vote_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='vote',folder=folder)
            vote_list=vote_data.get('record')
            if vote_list != None and len(vote_list) >0:
                if not(session_type in vote_result):
                    vote_result[session_type]=[]
                
                for item in vote_list:
                    turn=item.get('turn',0)
                    turn_vote_result={}
                    for key,vote_item in item.get('vote').items():
                        role=vote_item.get('role')
                        add_to_dict(turn_vote_result,role,1)
                    if (len(turn_vote_result)>0):
                        add_to_dict(turn_record,turn,1)
                            
                        out_key=max(turn_vote_result, key=turn_vote_result.get)
                        
                        turn_result={'turn':turn,'out':out_key,'data':turn_vote_result}
                        vote_result[session_type].append(turn_result)
                    
        
        # analyze session
        session_result={}
        for key,item in vote_result.items():
            
            overall_vote_result={}
            overall_out_result={}
            single_turn_result=[]
            turn_result=[]
            for turn in turn_record.keys():
                votes=[x for x in item if x.get('turn') == turn]
                turn_vote_result={}
                turn_out_result={}
                for vote in votes:
                    for role,count in vote.get('data').items():
                        add_to_dict(turn_vote_result,role,count)
                        add_to_dict(overall_vote_result,role,count)
                    add_to_dict(turn_out_result,vote.get('out'),1)
                    add_to_dict(overall_out_result,vote.get('out'),1)
                    single_turn_result.append(norm(vote.get('data')))
                turn_result.append({'turn':turn,'vote':norm(turn_vote_result),'out':norm(turn_out_result)})
            
            single_std=sum([x.get('std') for x in single_turn_result])/len(single_turn_result)
            single_var=sum([x.get('var') for x in single_turn_result])/len(single_turn_result)
            session_result[key]={'vote':norm(overall_vote_result),'out':norm(overall_out_result),'turn':turn_result,'single_turn':single_turn_result,'single_std':single_std,'single_var':single_var}
                    
        
        final_result={'vote_result':vote_result,'session_result':session_result}
        
        print(">> STD Result:")
        for session,data in session_result.items():
            print(f">>> {session} std : {data.get('single_std'):.3f}>> ")
        # print(">> STD Result By Turn")
        # for session,data in session_result.items():
        #     print(f">>> {session} >> ")
        #     for turn_data in data.get('turn'):
        #         print(f" T{turn_data.get('turn')} {turn_data.get('vote').get('std')}")
        #     print(f"All: {data.get('vote').get('std')}")
        print(">> Vote Result All(Judgement Variaion) ")
        for session,data in session_result.items():
            print(f">>> {session} >> ")
            # for turn_data in data.get('turn'):
            #     print(f" T{turn_data.get('turn')} {turn_data.get('vote')}")
            score = 1.0 / data.get('vote').get('std')
            print(f"All: {score:.3f}") 
               
        print("Output csv...")
        sessions=list(session_result.keys())
        
        content = ""
        content +="," + ",".join(sessions) +"\n"
        content +="JudgementVariation"
        for session in sessions:
            score = 1.0 / session_result[session].get('vote').get('std')
            content += f",{score:.3f}"
        print(content)
        
        print(">> Vote Result By Role All ")
        for session,data in session_result.items():
            print(f">>> {session} >> ")
            print(f" T{data.get('vote')}")
            
        print("Output csv...")
        content=","
        role_list=['seer','villager','villager_','mason','mason_','minion','tanner','werewolf']
        # session_list=['base','bigfive','bigfive_favor','next_strategy','full']
        
        session_list=list(session_result.keys())
        content=""
        for role in role_list:
            content+=","+role
        content+="\n"
        for se_key in session_list:
            data=session_result[se_key]
            content+=se_key.replace("werewolf_","")
            for role in role_list:
                content+=","+str(data.get('vote').get(role))
            content+="\n"
            # print(content)
        
        print(content)
        
        Global.file_save(output_file.replace(".json",".csv"),content)    
        Global.json_save(output_file,final_result)

    @staticmethod
    def analyze_LLM(folder,analyze_type):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        output_file=f"{GlobalSettings.STORAGE_PATH}/{folder}/analyze_llm.json"
        
        def get_value(data):
            result=data.get('result',[])
            if len(result) > 0:
                value=0
                count=0
                for item in result:
                    value=value+float(item.get('value'))
                    count=count+1
                return value / count 
                    
            return 0

        def get_interest(data):
            result=data.get('result',[])
            if len(result) > 0:
                value=0
                count=0
                for item in result:
                    value=value+float(item.get('value'))
                    count=count+1
                return value / count 
                    
            return 0
        
        def deal_mem(data_session,data_dict):
            result=data_session.get('result',[])
            
            if data_dict is None:
                data_dict={
                    "score":{"Werewolf":0,"Seer":0,"Minion":0,"Villager":0,"Mason":0,"Tanner":0},
                    "count":{"Werewolf":0,"Seer":0,"Minion":0,"Villager":0,"Mason":0,"Tanner":0},
                    'Ave':[]}
                
            if len(result) > 0:
                for result_item in result:
                    role_score=result_item.get('role_expect')
                    for role,score in role_score.items():
                        if role in data_dict["score"]:
                            data_dict["score"][role]+=score
                    role_count=result_item.get('role')
                    for role,count in role_count.items():
                        if role in data_dict["count"]:
                            data_dict["count"][role]+=count
                    data_dict['Ave'].append(result_item.get('average'))        
                    
            return data_dict
        
        role_norm={"Werewolf":1.0,"Seer":1.0,"Minion":1.0,"Villager":0.5,"Mason":0.5,"Tanner":1.0}
        def cal_mem(data_dict):
            role_score_dict=dict()
            for role in role_norm.keys():
                if role in data_dict["score"]:
                    role_score_dict[role]=data_dict["score"][role] # *role_norm[role]
                else:
                    role_score_dict[role]=0
                    
                # if 'Mason'==role or 'Villager'==role:
                #     role_score_dict[role+'_']=role_score_dict[role]
                    
            ave_role_score_dict=dict()
            for role in role_norm.keys():
                if role in data_dict["score"]:
                    ave_role_score_dict[role]=data_dict["score"][role]/data_dict["count"][role]
                else:
                    ave_role_score_dict[role]=0
                    
            
            array=np.array(list(ave_role_score_dict.values()))
            ave_role_std=10/array.std()
            
            array=np.array(list(role_score_dict.values()))
            role_std=10000/array.std()
            
            ave_array=np.array(data_dict['Ave'])
            mem_mean=ave_array.mean()
            
            return role_std
        
        def get_mem(data_session):
            result=data_session.get('result',[])
            
            if len(result) > 0:
                mean_list=[]
                std_list=[]
                score_dict_list=[]
                for result_item in result:
                    # role_data=result_item.get('role')
                    if not('role_expect' in result_item ):
                        role_data=dict()
                        for item in result_item.get('data'):
                            role=item.get('role')
                            score=float(item.get('score'))
                            if role in role_data:
                                role_data[role]+=score
                            else:
                                role_data[role]=score
                    else:
                        role_data=result_item.get('role_expect')
                        
                    score_dict=dict()
                    for role in role_norm.keys():
                        if role in role_data:
                            score_dict[role]=role_data[role]*role_norm[role]
                        else:
                            score_dict[role]=0
                            
                        if 'Mason'==role or 'Villager'==role:
                            score_dict[role+'_']=score_dict[role]
                    
                    array=np.array(list(score_dict.values()))
                    mean=array.mean()
                    std=100/array.std()
                    mean_list.append(mean)
                    std_list.append(std)
                    score_dict_list.append(score_dict)
                    
                mean=np.array(mean_list).mean()
                std=np.array(std_list).mean()
                
                return mean
                # return std
            return 0 
                # print(score_dict_list)
                
                # return (mean,std,score_dict_list)
            # return (0,0,[])
        
        def content_distance(from_dict,to_dict):
            distance=0
            names=list(from_dict.keys())
            for s in names:
                for t in names:
                    if s != t:
                        fr=from_dict[s][t]
                        tr=to_dict[s][t]
                        if fr==tr:
                            distance+=0
                        elif fr=='none' or tr=='none':
                            distance+=1.0
                        else:
                            distance+=2.0  
            return distance  
            
        def get_variation_list(data_from_file):
            result_list=data_from_file.get('result',[])
            turn_result_list=[]
            if len(result_list) > 0:
                for data in result_list:
                    turn_list=data.get('result_list',[])
                    for turn_data in turn_list:
                        turn_result=turn_data.get('result',{})
                        turn_result_list.append(turn_result)
            return turn_result_list
            
        def cal_variation_from_list(turn_result_list):
            distance_list=[]
            count=len(turn_result_list)   
            for i in range(count):
                for j in range(count):
                    if i != j:  
                      distance_list.append(content_distance(turn_result_list[i],turn_result_list[j]))
                
            return np.array(distance_list).mean()
        
            
        def get_variation(data_session):
            turn_result_list=get_variation_list(data_session)
            return  cal_variation_from_list(turn_result_list)
            # distance_list=[]
            # count=len(turn_result_list)   
            # for i in range(count):
            #     for j in range(count):
            #         if i != j:  
            #           distance_list.append(content_distance(turn_result_list[i],turn_result_list[j]))
                
            # return np.array(distance_list).mean()
                
        llm_result=dict()
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            if not(session_type in llm_result):
                llm_result[session_type]={'attraction':[],'interest':[],'surprise':[],'memorization':[],'variation_inner':[],'variation_all':[]}
                
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            
            attraction_value=0
            if analyze_type=="*" or 'attraction' in analyze_type:
                human_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_attraction',folder=folder)
                attraction_value=get_value(human_data)
                
            interest_value=0
            if analyze_type=="*" or 'interest' in analyze_type:
                interest_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_interest',folder=folder)
                interest_value=get_value(interest_data)
                
            surprise_value=0
            if analyze_type=="*" or 'surprise' in analyze_type:
                surprise_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_surprise',folder=folder)
                surprise_value=get_value(surprise_data)
            
            # mem_value=0
            # if analyze_type=="*" or 'mem' in analyze_type:
            #     mem_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_mem',folder=folder)
            #     mem_value=get_mem(mem_data)
                
            var_value=0
            if analyze_type=="*" or 'variation' in analyze_type:
                
                var_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_variation',folder=folder)
                var_value=get_variation(var_data)
            
            # s_result={'attraction':attraction_value,'interest':interest_value,'surprise':surprise_value,'memorization':mem_value,'variation_s':var_value}

            llm_result[session_type]['attraction'].append(attraction_value)
            llm_result[session_type]['interest'].append(interest_value)
            llm_result[session_type]['surprise'].append(surprise_value)
            llm_result[session_type]['variation_inner'].append(var_value)
        
        if analyze_type=="*" or 'mem' in analyze_type:
            mem_expects=dict()
            for session in f_sessions:
                session_type=session[0]
                session_folder=session[1]
                
                mem_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_mem',folder=folder)
                if not session_type in mem_expects:
                    mem_expects[session_type]=None   
                mem_expects[session_type]=deal_mem(mem_data,mem_expects[session_type])
                
            for key,item in mem_expects.items():
                score=cal_mem(mem_expects[key])
                llm_result[key]['memorization']=[score]
                
        if analyze_type=="*" or 'variation' in analyze_type:
            var_list=dict()
            for session in f_sessions:
                session_type=session[0]
                session_folder=session[1]
                var_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name='evaluate_variation',folder=folder)
                if not session_type in var_list:
                    var_list[session_type]=[]
                turn_list=get_variation_list(var_data)
                var_list[session_type]+=turn_list
                
            for key,item in var_list.items():
                score=cal_variation_from_list(item)
                llm_result[key]['variation_all']=[score]
                
            
        # analyze session data
        session_analyze={}
        for session,item in llm_result.items():
            attraction_mean=np.array([x for x in item.get('attraction')]).mean()
            interest_mean=np.array([x for x in item.get('interest')]).mean()
            surprise_mean=np.array([x for x in item.get('surprise') ]).mean()
            mem_mean=np.array([x for x in item.get('memorization')]).mean()
            var_a_mean=np.array([x for x in item.get('variation_all')]).mean()
            var_i_mean=np.array([x for x in item.get('variation_inner')]).mean()
            session_analyze[session]={'attraction':attraction_mean,'interest':interest_mean,'surprise':surprise_mean,'memorization':mem_mean,'variation_inner':var_i_mean,'variation_all':var_a_mean}
        
        final_result={'data':llm_result,'analyze':session_analyze}
        
        for session,data in session_analyze.items():
            print(f" {session} >>>> \n    Attraction:{data.get('attraction'):.3f} \n    Engagement:{data.get('interest'):.3f} \n    Wonder:{data.get('surprise'):.3f} \n    Memoriability:{data.get('memorization'):.3f} \n    VariationInner:{data.get('variation_inner'):.3f} VariationAll:{data.get('variation_all'):.3f}")
        
        session_list=['base','bigfive','bigfive_favor','next_strategy','full']
        evaluation_list=['interest','surprise','attraction','memorization','variation_inner','variation_all']
        
        print("Print as csv ..")
        content=""
        for eva_key in evaluation_list:
            content+=","+eva_key
        # print(content)
        content+="\n"
        for se_key in session_list:
            data=session_analyze['werewolf_'+se_key]
            content+=se_key.replace("werewolf_","")
            for e in evaluation_list:
                content+=","+str(data.get(e))
            # print(content)
            content+="\n"
        
        print(content)
        Global.file_save(output_file.replace(".json",".csv"),content)        
        Global.json_save(output_file,final_result)
            
    @staticmethod
    def check_validation(folder):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        def log_error(session_folder,content):
            print(f"{session_folder} Error! {content}")
        
        all_count=dict()
        count_dict=dict()
        
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            is_success=True
            if not session_type in all_count:
                all_count[session_type]=1
            else:
                all_count[session_type]+=1
            
            # check dialog 
            # dialog_data = AnalyzeManager.get_analyze_data(session=session_folder,file_name='dialog',folder=folder)
            
            # if not( 'record' in dialog_data ):
            #     is_success=False
            #     log_error( session_folder,"Cannot find 'record' in data")
            # else:
            #     dialog_data=dialog_data.get('record')
            #     dialog_count=len(dialog_data)
            #     if not( dialog_count == 24):
            #         is_success=False
            #         log_error( session_folder,f"Invalide dialog count: {dialog_count}(should be 24)")
                
            # for i in range(24):
            #     personal=dialog_data[i].get('sender_personal')
            #     role_tips=personal.split('.')[0]
            #     role_tips=role_tips.split(' ')[-1]
            #     role=role_tips.lower()
            #     dialog_data[i]['sender_role']=role
            
            # file_path=f"{GlobalSettings.STORAGE_PATH}/{folder}/{session[1]}/analyze/dialog.json"
            # Global.json_save(file_path,{'record':dialog_data})
    
            # Check Evaluation
            evaluation_output_list=['evaluate_attraction','evaluate_interest','evaluate_mem','evaluate_surprise','evaluate_variation']
            
            # print(f"[{session_folder}] Check Result :")    
            for ef in evaluation_output_list:
                check_data=AnalyzeManager.get_analyze_data(session=session_folder,file_name=ef,folder=folder)
                if len(check_data) < 1:
                    is_success=False
                    log_error( session_folder,f"Cannot find file {ef}.json")     
                elif not('result' in check_data):
                    is_success=False
                    log_error( session_folder,f"Cannot find 'result' in file {ef}.json")
                else:
                    count=len(check_data.get('result'))
                    # print(f" >>>  {ef} has {count}")    
                

            if is_success:
                # print(f"{session_folder} passed validation!")
                if not session_type in count_dict:
                    count_dict[session_type]=1
                else:
                    count_dict[session_type]+=1
                    
        for key, allCount in all_count.items():
            if key in count_dict:
                count=count_dict[key]
            else:
                count=0
            print(f"[{key}] Valid:({count}/{allCount})")
            
    @staticmethod
    def check_dialog_result(folder):
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        
        def log_error(session_folder,content):
            print(f"{session_folder} Error! {content}")
        
        all_count=dict()
        count_dict=dict()
        
        for session in f_sessions:
            session_type=session[0]
            session_folder=session[1]
            
            if not session_type in all_count:
                all_count[session_type]=1
            else:
                all_count[session_type]+=1
                    
            is_success=True
            
            # check dialog 
            dialog_data = AnalyzeManager.get_analyze_data(session=session_folder,file_name='dialog',folder=folder)
            
            if not( 'record' in dialog_data ):
                is_success=False
                log_error( session_folder,"Cannot find 'record' in data")
            else:
                dialog_data=dialog_data.get('record')
                dialog_count=len(dialog_data)
                if not( dialog_count == 24):
                    is_success=False
                    log_error( session_folder,f"Invalide dialog count: {dialog_count}(should be 24)")
                

            if is_success:
                # print(f"{session_folder} passed validation!")
                if not session_type in count_dict:
                    count_dict[session_type]=1
                else:
                    count_dict[session_type]+=1
        
        for key, allCount in all_count.items():
            if key in count_dict:
                count=count_dict[key]
            else:
                count=0
            print(f"[{key}] Valid:({count}/{allCount})")