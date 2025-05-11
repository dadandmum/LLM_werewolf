
from lib.mglobal.global_function import Global
from lib.mission.mission_function import MissionFunction
from lib.keys_manager import keys_manager
from settings import GlobalSettings
import argparse, os, shutil

def get_args():
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-e","--environment",default="werewolf_base",help="name of environment setting json",type=str)
    parser.add_argument("-f","--folder",default="default",help="the name of subfolder",type=str)
    args=parser.parse_args()
    
    return args
    

def run_mission(env,folder='',delay=0):
    
    import time
    time.sleep(delay)
    
    print(f"[Main] Now start run env {env} ")
    keys_manager.setup()
    # load data from file
    env_info=Global.load_env(env)
    if env_info is None:
        print(f"[Error] Cannot find environment infomation file by environment '{env}'")
        return 
    mission_name=env_info.get("mission",None)
    if mission_name is None:
        print(f"[Error] Cannot find mission name from '{env}'")
        return 
    
    # setup session
    session=env_info.get("session","temp")
    if not(folder=='' or folder is None):
        session=f"{folder}/{session}"
    cover_old=env_info.get("cover_old_session",True)
    if cover_old:
        GlobalSettings.SetSession(session)
        session_dir=Global.get_storage_path("")
        if os.path.isdir(session_dir):
            shutil.rmtree(session_dir)
    else:
        session+=Global.get_now_time_block_format("_%Y-%m-%d-%H-%M-%S")
        GlobalSettings.SetSession(session)
    
    # setup settings
    settings=env_info.get("settings",{})
    for key,value in settings.items():
        GlobalSettings.SetSetting(key,value)
        
    # set up mission manager
    mission_file=env_info.get("mission_file",None)
    mission_manager=MissionFunction.get_mission_manager(mission_name,mission_file,False)
    mission_manager.start_mission(env_info)
    max_step=GlobalSettings.MISSION_MAX_STEP
    
    for index in range(max_step):
        mission_manager.next_step(index)
        if mission_manager.check_end_mission():
            break
    
    mission_manager.finish_mission()
        

def main():
    args=get_args()
    env=args.environment
    folder=args.folder
    run_mission(env=env,folder=folder)
    

if __name__ == '__main__':
    main()