import re 
import random

class BigFivePersona:
        
    NEO5_DATA_PATH="../data/persona/NEO5.csv"
    DEFINE_BF5_DATA_PATH="../data/persona/DescBF5.csv"
    FACTOR_LEVEL_RANGE=(1,7)
    
    FACTOR_TABLE=[
        {
            'level':1,
            'attitude':['strongly disagree','totally disagree'],
            'ne-attitude':['strongly agree','totally agree'],
            'degree':['extremely','incredibly','remarkably'],
            'attitude_count':(0,2),
            'define_count':(1,4),
        },
        {
            'level':2,
            'attitude':['disagree','quite disagree'],
            'ne-attitude':['agree','quite agree'],
            'degree':['very','totally','pretty'],
            'attitude_count':(0,1),
            'define_count':(0,2),
        },
        {
            'level':3,
            'attitude':['slightly disagree','fairly disagree','probably disagree'],
            'ne-attitude':['slightly agree','fairly agree','probably agree'],
            'degree':['slightly','fairly','quite'],
            'attitude_count':(0,1),
            'define_count':(0,1),
        },
        {
            'level':4,
            'attitude':['neighter agree or disagree'],
            'ne-attitude':['neighter agree or disagree'],
            'degree':['barely','never'],
            'attitude_count':(0,0),
            'define_count':(0,0),
        },
        {
            'level':5,
            'attitude':['slightly agree','fairly agree','probably agree'],
            'ne-attitude':['slightly disagree','fairly disagree','probably disagree'],
            'degree':['slightly','fairly','quite'],
            'attitude_count':(0,1),
            'define_count':(0,1),
        },
        {
            'level':6,
            'attitude':['agree','quite agree'],
            'ne-attitude':['disagree','quite disagree'],
            'degree':['very','totally','pretty'],
            'attitude_count':(0,1),
            'define_count':(0,2),
        },
        {
            'level':7,
            'attitude':['strongly agree','totally agree'],
            'ne-attitude':['strongly disagree','totally disagree'],
            'degree':['extremely','incredibly','remarkably'],
            'attitude_count':(0,2),
            'define_count':(1,4),
        }
        
    ]
    
    ATTITUDE=[('strongly disagree',0),
              ('little disagree',0.25),
              ('neighter agree or disagree',0.5),
              ('little agree',0.75),
              ('strongly agree',1.00)]
    CONDITION=['very',
               'a little',
               'barely',
               'a little',
               'very']
    
    
    DESCRIPTION_COUNT=3
    
    @staticmethod
    def get_big_five_attitude_data():
        with open(BigFivePersona.NEO5_DATA_PATH,'r') as file:
            content=file.read()
        lines=content.splitlines()
        items=[]
        for line in lines:
            items.append(line.split(','))
            
        data={}
        for item in items:
            key=item[4]
            if not(key) in data:
                data[key]=[]
            data[key].append((int(item[2]),item[3]))
           
        return data 
    
    @staticmethod
    def get_big_five_define_data():
        with open(BigFivePersona.DEFINE_BF5_DATA_PATH,'r') as file:
            content=file.read()
        lines=content.splitlines()
        items=[]
        data={}
        for line in lines:
            items = line.split(',')
            if len(items) > 2:
                if float(items[1]) > 0 :
                    data[f"{items[0]}+1"]=items[2:]
                else:
                    data[f"{items[0]}-1"]=items[2:]
                    
            
        return data 
        
    @staticmethod
    def get_rand_big_five_trait():
        result={}
        result['Agreeableness']=BigFivePersona.get_rand(BigFivePersona.FACTOR_LEVEL_RANGE)
        result['Extraversion']=BigFivePersona.get_rand(BigFivePersona.FACTOR_LEVEL_RANGE)
        result['Neuroticism']=BigFivePersona.get_rand(BigFivePersona.FACTOR_LEVEL_RANGE)
        result['Openness']=BigFivePersona.get_rand(BigFivePersona.FACTOR_LEVEL_RANGE)
        result['Conscientiousness']=BigFivePersona.get_rand(BigFivePersona.FACTOR_LEVEL_RANGE)
        return result
    
    @staticmethod
    def get_rand(range):
        return random.randrange(range[0],range[1]+1)
    
    @staticmethod
    def trait_to_description(trait):
        bf_att_data=BigFivePersona.get_big_five_attitude_data()
        bf_define_data=BigFivePersona.get_big_five_define_data()
        
        description=""
        # update IPIP attitude description
        for factor,value in trait.items():
            factor_item=BigFivePersona.FACTOR_TABLE[value-1]
            
            count=BigFivePersona.get_rand(factor_item.get('attitude_count'))
            # attitude_index_list=[value-1]*count
            att_content_list=random.sample(bf_att_data[factor],count)
            for index in range(count):
                if att_content_list[index][0] > 0:
                    attitude=random.choice(factor_item.get('attitude'))
                else:
                    attitude=random.choice(factor_item.get('ne-attitude'))
                # attitude_id=attitude_index_list[index] if des_list[index][0]>0 else len(BigFivePersona.ATTITUDE)-1-attitude_index_list[index]
                # attitude=random.sample(factor_item.get('attitude'),1)[0]
                content=att_content_list[index][1]
                description+=f"You {attitude} that you {content}\n"
                
            description+="\n"
                
        # update define description
        for factor,value in trait.items():
            factor_item=BigFivePersona.FACTOR_TABLE[value-1]
            count=BigFivePersona.get_rand(factor_item.get('define_count'))
            degree_list=factor_item.get('degree')
            #for index in range(count):
            if count > 0:
                if value >=4: # use positive adj
                    define_list=random.sample(bf_define_data[f"{factor}+1"],count)
                else: # use negative adj 
                    define_list=random.sample(bf_define_data[f"{factor}-1"],count)
                if len(define_list) > 0 :
                    final_list=[f"{random.choice(degree_list)} {x}" for x in define_list]
                    adj=", ".join(final_list)
                    description+= f"You speak in a {adj} way."
                
        return description

    @staticmethod
    def get_rand_big_five_description():
        trait=BigFivePersona.get_rand_big_five_trait()
        return (trait,BigFivePersona.trait_to_description(trait=trait))