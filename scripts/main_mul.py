import subprocess
import main
import argparse
from threading import Thread
from multiprocessing import Process
from multiprocessing import Pool
from settings import GlobalSettings

def get_args():
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-e","--environment",default="werewolf_base",help="list of names of environment setting json(split by ',' )",type=str)
    parser.add_argument("-f","--folder",default="default",help="the name of subfolder",type=str)
    parser.add_argument("-c","--count",default=5,help="the total number of each environment",type=int)
    args=parser.parse_args()
    
    return args

    
def run_mission_mul(envs,folder,count):
    max_process=GlobalSettings.MAX_PROCESS
    params=[]
    delay=0
    for i in range(count):
        for env in envs:
            params.append((env,folder,delay))
            delay+=1.5
    print(params)
    with Pool(max_process) as p:
        p.starmap(func=main.run_mission,iterable=params)

def main_mul():
    args=get_args()
    envs=args.environment.split(",")
    folder=args.folder
    count=args.count
    run_mission_mul(envs,folder,count)

if __name__ == '__main__':
    main_mul()