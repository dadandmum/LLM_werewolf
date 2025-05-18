
import wordcloud
import argparse, os , re 
from settings import GlobalSettings
from lib.mglobal.global_function import Global
import colorsys, random 


def get_args():
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-f","--folder",default="temp",help="the name of subfolder",type=str)
    parser.add_argument("-s","--session",default="none",help="the name of session",type=str)
    args=parser.parse_args()
    
    return args
    
class GenWC:
    wc_color_index=-1
    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def get_color_range(word,**kwargs):
        h = GenWC.wc_color_index
        s = random.uniform(0.4,0.9)
        v = random.uniform(0.1,0.5)

        return GenWC.hsv2rgb(h,s,v)
        
    def draw_wordcloud(content,output,color_index=0):
        GenWC.wc_color_index=color_index
        wc=wordcloud.WordCloud(
            font_path="../data/fonts/arial.ttf",
            width=800,
            height=800,
            background_color="white",
            color_func=GenWC.get_color_range)
        wc.generate(content)
        wc.to_file(output)
    
def run_wc_session(folder='temp',session='none'):
    ana_root=f"{GlobalSettings.STORAGE_PATH}/{folder}/{session}/analyze"
    all_files=os.listdir(ana_root)
    
    for file in all_files:
        pattern="agent_([a-zA-Z]+)_dialog.txt"
        find=re.findall(pattern,file)
        
        if len(find) > 0:
            agent=find[0]
            content=Global.file_load(f"{ana_root}/{file}")
            output_file=f"{ana_root}/agent_{agent}_wordcloud.png"
            index=random.uniform(0,1)
            
            GenWC.draw_wordcloud(content=content,output=output_file,color_index=index)
            
    
    
def main():
    args=get_args()
    folder=args.folder
    session=args.session
    
    if session=='none':
        folder_root=f"{GlobalSettings.STORAGE_PATH}/{folder}"
        all_sessions=os.listdir(folder_root)
        session=all_sessions[0]
        print(f"run session {session}...")
            
    run_wc_session(session=session,folder=folder)
    

if __name__ == '__main__':
    main()