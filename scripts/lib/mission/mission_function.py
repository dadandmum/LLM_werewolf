from lib.mglobal.global_function import GlobalSettings
import os
from lib.mission.manager.talk_weather import TalkWeather
from lib.mission.manager.werewolf import Werewolf
from lib.mission.manager.werewolf_B5P import WerewolfB5P
from lib.mission.manager.werewolf_favor import WerewolfFavor

class MissionFunction:
    @staticmethod
    def get_all_missions():
        mission_path=GlobalSettings.MISSION_PATH
        mission_list=[]
        for file in os.listdir(mission_path):
            if file.endswith('.txt'):
                mission_list.append(file.strip('.txt'))
        return mission_list
    
    
    @staticmethod
    def get_mission_manager(mission,mission_file=None,debug=True):
        if mission_file==None:
            mission_file=mission
        if mission == "weather":
            return TalkWeather(mission,mission_file,debug)
        elif mission == "werewolf":
            return Werewolf(mission,mission_file,debug)
        elif mission == "werewolfB5P":
            return WerewolfB5P(mission,mission_file,debug)
        elif mission == "werewolfFavor":
            return WerewolfFavor(mission,mission_file,debug)
        