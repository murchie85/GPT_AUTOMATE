import os 
import openai
from termcolor      import colored, cprint 

def getOpenAPIKey():
    
    # ----------------- CALL OPEN AI
    
    if os.environ.get("OPENAI_API_KEY"):
        cprint('Loading Key from Environment variable','yellow')
        openai.api_key = os.environ["OPENAI_API_KEY"]
    else:
        cprint('No key in env vars, attempting to load from file ','yellow')
        keyFile = open('/Users/adammcmurchie/code/tools/davinci/.KEY.txt','r')
        #keyFile = open('.TOKEN.txt','r')
        openai.api_key      = keyFile.read()
    
    print('')
    cprint('Loaded','white')
    print('') 

    return(openai)