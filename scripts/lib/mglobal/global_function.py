import datetime as dt
import os
import json
import re
from datetime import datetime, timezone, timedelta
from os import listdir
from filelock import FileLock, Timeout
from settings import GlobalSettings

class Global:
    @staticmethod
    def clean_dialog_content(content,title):
        """
        Clean the unneccessary char in content

        Args:
            content (string): dialog content to clean
            title (string): title of the dialog sender 

        Returns:
            string: the cleaned dialog with no dirty chars
        """
        data=content
        data=data.strip(' ').strip('“').strip('”').strip('"').strip("'")
        data=data.strip(title+":").strip(title+"：")
        data=data.strip(' ').strip('“').strip('”').strip('"').strip("'")
        
        return data
    
    @staticmethod
    def create_folder_if_not_there(curr_path):
        """
        Checks if a folder in the curr_path exists. If it does not exist, creates
        the folder.

        Args:
            curr_path (_type_): path to write. 

        Returns:
            None 
        """
        outfolder_name=curr_path.split("/")
        if len(outfolder_name) != 1:
            # This checks if the curr path is a file or a folder.
            if "." in outfolder_name[-1]:
                outfolder_name=outfolder_name[:-1]
                
            outfolder_name="/".join(outfolder_name)
            if not os.path.exists(outfolder_name):
                os.makedirs(outfolder_name)
                return True
        return False
    
    
    @staticmethod
    def check_if_file_exists(curr_file):
        """
        Check if a file exists

        Args:
            curr_file (_type_): path to current file
        Returns:
            True if the file exists
            False if the file does not exists
        """
        try:
            with open(curr_file) as f:pass
            return True
        except:
            return False
        
        
        
    @staticmethod
    def json_add_item_to_list(file_path,key,item):
        """
            Add an item to a list by the key
            {
                "key": [...,..., +item+ ]
            }
            the file edition is thread safe 
        Args:
            file_path (string): output path of the file
            key (string): the key of the item in the json file
            item (object): the item to add to the list
        """
        Global.create_folder_if_not_there(file_path)
        data={}
        if Global.check_if_file_exists(file_path):
            lock = FileLock(file_path+".lock")
            try:
                with lock.acquire(timeout=5):
                    data={}
                    with open(file_path,'r',encoding='utf-8') as f:
                        data=json.load(f)
                    if not(key in data):
                        data[key]=[]
                    data[key].append(item)
                    with open(file_path,'w',encoding='utf-8') as f:
                        json.dump(data,f)
            except Timeout:
                print('[json_add_item_to_list] Timeout!')
        else:
            lock=FileLock(file_path+".lock")
            with lock:
                with open(file_path,'w',encoding='utf-8') as f:
                    data={}
                    data[key]=[]
                    data[key].append(item)
                    json.dump(data,f)
           
    @staticmethod
    def json_update(file_path,in_data):
        """
        update the json file with data 

        Args:
            file_path (string ): file path
            in_data (json): data to update 
        """
        
        Global.create_folder_if_not_there(file_path)
        data={}
        if Global.check_if_file_exists(file_path):
            lock = FileLock(file_path+".lock")
            try:
                with lock.acquire(timeout=5):
                    with open(file_path,'r',encoding='utf-8') as f:
                        data=json.load(f)
                    data.update(in_data)
                    with open(file_path,'w',encoding='utf-8') as f:
                        json.dump(data,f)
            except Timeout:
                print('[json_update] Timeout!')
        else:
            lock=FileLock(file_path+".lock")
            with lock:
                with open(file_path,'w',encoding='utf-8') as f:
                    data.update(in_data)
                    json.dump(data,f)       
    
    @staticmethod
    def json_load(file_path):
        """
        load json from file
        Args:
            file_path (string): load json from file 
        """
        data = {}
        
        if Global.check_if_file_exists(file_path):
            with open(file_path,'r',encoding='utf-8') as f:
                data = json.load(f)
            
        return data
            
            
    @staticmethod
    def json_save(file_path,data):
        """
        save json to file
        Args:
            file_path (string): save json to file 
            data (json): json data 
        """
        Global.create_folder_if_not_there(file_path)
        
        with open(file_path,"w",encoding='utf-8') as outfile:
            json.dump(data,outfile)
                        

    @staticmethod
    def file_save(file_path,content):
        """
        save content to file
        Args:
            file_path (string): save text to file 
            content (string): text data 
        """
        Global.create_folder_if_not_there(file_path)
        
        with open(file_path,"w",encoding='utf-8') as outfile:
            outfile.write(content)
       
    @staticmethod
    def file_remove(file_path):
        
        if Global.check_if_file_exists(file_path):
            os.remove(file_path)
            return True
            
        return False
       
    @staticmethod
    def file_load(file_path):
        """
        load text from file
        Args:
            file_path (string): load text from file
        """
        data = {}
        
        if Global.check_if_file_exists(file_path):
            with open(file_path,'r',encoding='utf-8') as f:
                data = f.read()
            
        return data
            
                 
    @staticmethod
    def write_to_file_append(file_path,content):
        Global.create_folder_if_not_there(file_path)
        if Global.check_if_file_exists(file_path):
            lock = FileLock(file_path+".lock")
            try:
                with lock.acquire(timeout=5):
                    data={}
                    with open(file_path,'a',encoding='utf-8') as f:
                        f.write(content)
            except Timeout:
                print('[write_to_file] Timeout!')
        else:
            lock=FileLock(file_path+".lock")
            with lock:
                with open(file_path,'w',encoding='utf-8') as f:
                    f.write(content)

    @staticmethod
    def load_agent_info(agent_id) ->json :
        info_path = f"{GlobalSettings.AGENT_INFO_PATH}/{agent_id}.json"
        return Global.json_load(info_path)
    
    @staticmethod
    def load_task(task) -> str :
        file_path = f"{GlobalSettings.TASK_PATH}/{task}.txt"
        template=""
        if Global.check_if_file_exists(file_path):
            with open(file_path,'r',encoding='utf-8') as f:
                template=f.read()
                
        return template
    
    @staticmethod
    def load_env(env_name)->json:
        file_path=f"{GlobalSettings.ENV_PATH}/{env_name}.json"
        return Global.json_load(file_path)
    
    @staticmethod
    def load_mission_info(mission_name)->json:
        file_path=f"{GlobalSettings.MISSION_PATH}/{mission_name}.json"
        return Global.json_load(file_path)
                    
    @staticmethod
    def get_storage_path(sub_folder)->str:
        return f"{GlobalSettings.STORAGE_PATH}/{GlobalSettings.SESSION}/{sub_folder}"
    
    @staticmethod
    def get_now_time():
        return int(datetime.now().timestamp())
    
    @staticmethod
    def get_time_daily():
        """
        Get Daily Time in Year - Month - Day

        Returns:
            string : return the time in YYYY-MM-DD
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_now_time_block():
        return datetime.now().astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    
    @staticmethod
    def get_now_time_block_format(format):
        """
        Format the time in GMT+8

        Example: "%d/%m/%Y, %H:%M:%S"
        """
        return datetime.now().astimezone(timezone(timedelta(hours=8))).strftime(format)
    
    @staticmethod
    def get_now_time_in_YMD_HMS():
        return datetime.now().astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d_%H:%M:%S")
    
    @staticmethod
    def filter_from_list(input,filter_content,index=0):
        filter_dict=re.findall("<(\w+),(\w+)>",filter_content)
        def replace_by_filter(input,find):
            for f in find:
                if input in f[0] or input in f[1] or f[0] in input or f[1] in input:
                    return f[index]
            return 'None'
        return replace_by_filter(input,filter_dict)       
    
    MISSION_INSTANCE = None
    
    @staticmethod
    def get_mission_instance():
        return Global.MISSION_INSTANCE
    
    @staticmethod
    def get_global_now_time_stamp():
        if Global.MISSION_INSTANCE is None:
            return Global.get_now_time()
        else:
            return Global.MISSION_INSTANCE.get_time_stamp()
        
    @staticmethod
    def clean_dialog_content(content,agent_name):
        data=content
        data=data.strip(' ').strip('“').strip('”').strip('"').strip("'")
        data=data.strip(agent_name+':').strip(agent_name+'：').strip(agent_name+' says：')
        data=data.strip(' ').strip('“').strip('”').strip('"').strip("'")
        
        return data
    
    
    @staticmethod
    def get_distribution_value(value,distribution,min_value=0):
        last_value=min_value
        for dist in distribution:
            if value >= last_value and value < dist[0]:
                return dist[1]
            
        return ''