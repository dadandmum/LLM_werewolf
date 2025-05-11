import sys

class GlobalSettings:
    # ======= Model ======
    # LLM_MODEL = "gpt-4o-mini"
    LLM_MODEL = "qwen-plus"
    # LLM_EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_EMBEDDING_MODEL = "text-embedding-v2"
    
    LLM_MODEL_DICT={
        # 'default':'gpt-3.5-turbo-0125',
        'default':'qwen-plus',
        'dialog':'qwen-plus',
        'gpt4o':'gpt-4o',
    }
    
    LLM_TASK_DICT={
        'generate_dialog':'dialog',
    }
    # ======== PATH ============
    AGENT_INFO_PATH = "../data/agent"
    TASK_PATH = "../data/task"
    MISSION_PATH = "../data/mission"
    ENV_PATH = "../data/env"
    
    STORAGE_PATH="../cache"
    SESSION="temp"
    
    @staticmethod 
    def SetSession(session):
        GlobalSettings.SESSION=session
        
    @staticmethod 
    def SetSetting(name,value):
        setattr(GlobalSettings,name,value)
    
    # ======== MISSION ============
    MISSION_MAX_STEP=1000
    TALK_WORD_LIMIT=120
    TALK_TURN=3
    MISSION_RECORD_TO_FILE=True
    
    # ======== SETTING ==========
    USE_MISSION_JUDGE=False
    UES_RANDOM_BIG_FIVE=True
    USE_FAVOR=False
    USE_NEXT_STRATEGY=True
    USE_ANALYZE=True
    REMEMBER_MEMORY_COUNT=8
    JUDGE_MEMORY_COUNT=8
    VOTE_MEMORY_COUNT=8
    FAVOR_MEMORY_COUNT=8
    DIALOG_MEMORY_COUNT=4
    USE_TURN_ANALYZE=True
    UPDATE_LAST_ACCESS=False
    MAX_PROCESS=20
    
    # ======== DEBUG =============
    
    USE_EMBEDDING=False
    DEBUG_LOG = True
    DEBUG_LOG_AGENT = True
    DEBUG_LOG_LLM = True
    
    DEBUG_LOG_LLM_MESSAGE=True
    
    DEBUG_MISSION_LOG=True
    
    
    # DEBUG_TASK=['generate_dialog']
    DEBUG_TASK=[]
    
    # ===========================
    USE_FAKE_DIALOG=False
    USE_FAKE_FAVOR=False
    