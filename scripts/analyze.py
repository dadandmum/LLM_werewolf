from settings import GlobalSettings
from lib.mglobal.global_function import Global
from lib.analyze.analyze_manager import AnalyzeManager
from lib.keys_manager import keys_manager
from multiprocessing import Pool

import argparse

def get_args():
    
    parser=argparse.ArgumentParser()
    # parser.add_argument("-e","--environment",default="test_weather",help="name of environment setting json",type=str)
    parser.add_argument("-s","--session",default="none",help="the session id, for single_embedding ",type=str)
    parser.add_argument("-f","--folder",default="none",help="the subfolder to analyze, for all tasks",type=str)
    parser.add_argument("-m","--model",default="default",help="the subfolder to analyze(gte-large;none), for generate_embedding",type=str)
    parser.add_argument("-t","--task",default="none",help="the analyze task:\n\r \
                                                            se/single_embedding : analyze the embedding(text distance) of a single session;\n \
                                                            me/multiple_embedding : analyze the embedding(text distance) of a folder; \n \
                                                            ge/generate_embedding : generate the embedding(text distance) of a folder; \n \
                                                            el/evaluate_LLM : generate the LLM-base evaluation for a folder; \n \
                                                            al/analyze_LLM : analyze the LLM-base evaluation for a folder; \n \
                                                            av/analyze_vote : analyze the vote result of a folder; \n \
                                                            cv/check_validation : check the result of a folder, check dialog or LLM-base evaluation(see check_type); \n \
                                                            ce/clean_evalution : clean all the evaulation result of a folder; \n\
                                                            sa/single_check_agent: check the agent result of a session; \n\
                                                            sav/simple_analyze_vote: for favor check, just analyze the vote result; \n\
                                                            ",type=str)
    parser.add_argument("-a","--analyze_type",default="*",help="the analyze type(reconginze first 3 letters): [int]erest;[sur]prise;[hum]an;[mem]orization;[var]iation;* for all",type=str)
    parser.add_argument("-c","--check_type",default="*",help="check types: dialog;llm;* for all",type=str)
    parser.add_argument("-et","--evaluation_time",default=1,help="loop time for llm evaluation",type=int)
    args=parser.parse_args()
    
    return args

def run_analyze(session,model,folder):
    AnalyzeManager.analyze_embedding_dialog(session=session,folder=folder,model=model)

def run_folder_analyze(folder,model):
    AnalyzeManager.analyze_embedding_folder(folder,model)
    
def generate_embedding(folder,model):
    AnalyzeManager.generate_embedding(folder=folder,model=model)
    
def generate_LLM_evaluate(folder):
    AnalyzeManager.generate_LLM_evaulate(folder)
    
def main():
    keys_manager.setup()
    
    args=get_args()
    session=args.session
    folder=args.folder
    model=args.model
    task=args.task
    check_type=args.check_type
    analyze_type=args.analyze_type
    evaluation_time=args.evaluation_time
    
    if task=="single_embedding" or task=="se":
        if session != 'none':
            AnalyzeManager.analyze_embedding_dialog(session=session,folder=folder,model=model)
        else:
            print("Unable to find parameter 'session' ")
    elif task=="multiple_embedding" or task=="me":
        if folder != 'none':
            AnalyzeManager.analyze_embedding_folder(folder,model)
        else:
            print("Unable to find parameter 'folder' ")
    elif task=="generate_embedding" or task=="ge":
        AnalyzeManager.generate_embedding(folder=folder,model=model)
    elif task=="evaluate_LLM"or task=="el":
        
        max_process=GlobalSettings.MAX_PROCESS
        f_sessions=AnalyzeManager.get_all_sessions(folder)
        params=[]
        for i in range(evaluation_time):
            for session in f_sessions:
                params.append((folder,session[1],analyze_type))
        print(params)
        with Pool(max_process) as p:
            p.starmap(func=AnalyzeManager.generate_LLM_evaluate_session,iterable=params)
        
        # AnalyzeManager.generate_LLM_evaulate(folder=folder,analyze_type=analyze_type)
    elif task=="analyze_LLM" or task=="al":
        AnalyzeManager.analyze_LLM(folder=folder,analyze_type=analyze_type)
    elif task=="analyze_vote" or task=="av":
        AnalyzeManager.analyze_vote(folder=folder)
    elif task=="simple_analyze_vote" or task=="sav":
        AnalyzeManager.simple_analyze_vote(folder=folder)
    elif task=="check_validation" or task=="cv":
        if check_type=="*" or "dialog" in check_type:
            AnalyzeManager.check_dialog_result(folder=folder)
        if check_type=="*" or "llm" in check_type:
            AnalyzeManager.check_validation(folder=folder)
    elif task=="single_check_agent" or task=="sa":
        AnalyzeManager.analyze_embedding_dialog_by_agent(session=session,folder=folder)
    elif task=="clean_evalution" or task=="ce":
        AnalyzeManager.clean_evalution(folder=folder,analyze_type=analyze_type)

if __name__ == '__main__':
    main()