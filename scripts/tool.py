
import os 
import sys
from llm_tool import run_tool
from lib.keys_manager import keys_manager

def main():
    keys_manager.setup()
    run_tool()
    

if __name__ == '__main__':
    main()