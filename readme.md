# Introduction

This is a project shows a group of LLM agents to play werewolf game.


# Quick Start

##  Install package 

```
pip install openai
pip install numpy
pip install filelock
pip install wordcloud
pip install matplotlib
pip install sentence_transformers
pip install pyside6
```

##  Set API key
1. Apply and Access API key from openai (https://platform.openai.com/account/api-keys) , qwen(https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api)

2. Set API key in the file `scripts/lib/keys_manager.py` as follows:

```
    OPEN_AI_KEY = "YOUR OPENAI API KEY"
    ALI_API_KEY = "YOUR QWEN API KEY" 
```

## Run a werewolf game

### Demo game
Run the bat file `bats/run_werewolf_demo.bat`

### Run Prompt Tool
Run the tool bat file `bat/run_tool.bat'. It will run an interactive window to test the prompt template.

### Run Full Game 
Run the bat file `bats/run_werewolf.bat`, the result will be saved to cache\temp\[the folder with task name and date]


# Reference
## OpenAI
https://platform.openai.com/docs/api-reference/chat/create
## Qwen
https://help.aliyun.com/zh/dashscope/developer-reference/api-details