import openai
import yaml
import re
import pprint 
from termcolor      import colored, cprint 


def generate_code(prompt):
    # ----------------- CALL OPEN AI

    keyFile = open(,'r')
    openai.api_key    = keyFile.read()

    availableResponses   = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}])
    currentResponse = availableResponses['choices'][0]['message']['content'].lstrip()
    return currentResponse

def process_deliverable(yaml_content, desired_deliverable):
    
    # Find the desired deliverable
    deliverable = None
    for d in yaml_content:
        if d['DELIVERABLE'] == desired_deliverable:
            deliverable = d
            break

    if deliverable is None:
        raise ValueError(f'DELIVERABLE: {desired_deliverable} not found.')

    location = 'output/' + deliverable['RUNTIME_INSTRUCTIONS']['LOCATION']
    filename = deliverable['RUNTIME_INSTRUCTIONS']['FILENAME']


    print("DESIRED DELIVERABLE IS ")
    print(desired_deliverable)
    print("LOCATION IS ")
    print(location)
    print("FILENAME IS ")
    print(filename)

    input('ready to generate code?')
    # Generate and append code in chunks of 400 lines
    code_chunk = None
    chunkCount = 0
    while code_chunk != "":
        prompt = f"You are given a YAML file that describes a project broken into multiple deliverables. Your task is to generate code for the specified deliverable in chunks of 400 lines at a time. DO NOT add any extra words, just provide only the code. If there is no more code to provide, just return ##JOB_COMPLETE## \n\nPlease process DELIVERABLE: {desired_deliverable}. \n\n{yaml_content}\n\nPreviously generated code (if any):\n{code_chunk}\n\nGenerate the next 400 lines:"
        cprint(prompt + '\n**prompt ends**', 'blue')

        # SENDING REQUEST
        cprint('Sending Request', 'yellow',attrs=['blink'])
        code_chunk = generate_code(prompt)
        chunkCount += 1
        print(code_chunk)
        cprint('Received, saving...', 'white')

        with open(f"{location}/{filename}", "a") as f:
            f.write(code_chunk)

        cprint('Saved', 'yellow')
        
        # 
        if('JOB_COMPLETE' in code_chunk):
            cprint('Job Complete', 'white')
            return()
        #input("Continue with next chunk? Number: " + str(chunkCount))
        if(chunkCount>5):
            print("Something likely went wrong - chunk at 400 * 5")
            input("Exit or continue?")



def decompose():
    # Usage:
    file_path = 'workspace/classifiedProblems.yaml'
    with open(file_path, 'r') as file:
        data = file.read()


    print('printing raw data')
    print(data)

    print('Printing as dict')
    yaml_content = yaml.safe_load(data)
    pprint.pprint(yaml_content)





    desired_deliverable = 0
    for n in range(len(yaml_content)):
        process_deliverable(yaml_content, n+1)
