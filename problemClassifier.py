import openai
from utils import *
from termcolor      import colored, cprint 
import re 
import os


class ProblemClassifier:
    def __init__(self):
        self.state                   = 'not_started'
        self.problem_state           = None
        self.run_count               = 0
        self.human_feedback_count    = 0
        self.fullDialogue            = ''
        self.currentResponse         = ''
        self.deliverableArray        = []
        self.problemStatement        = ''
        self.no_deliverables         = 0

    def get_requirements(self,openaiObject):

        # -----------------GET USER REQUIREMENT

        user_input = input("Please describe your problem: ")
        self.problemStatement = user_input
        
        # -----------------SAVE PROBLEM STATEMENT

        f = open('workspace/statement.txt','w')
        f.write(user_input)
        f.close()
        

        # -----------------CONSTRUCT THE PROMPT


        prompt = f"""
        This is an automation pipeline, please respond exactly as described below, do not deviate.
        First, quantify this problem: {user_input}
        If it cannot be solved by code, return only False and do not add any more information.
        If it can be solved by code, produce the high-level steps for the smallest seperate deliverable increments in the yaml format like below:

        - DELIVERABLE: 1
          Solution:
            - Set up backend server using Node.js and Express framework
            - Create database schema using MongoDB for storing blog data
            - Implement API endpoints for creating, editing, and deleting blogs
            - Implement user authentication using Passport.js
            - Build frontend using React library for displaying blogs and interacting with API
          Dependencies: Node.js, Express, MongoDB, React, Passport.js
          SharedState: N/A
          AdditionalNotes: N/A
          RUNTIME_INSTRUCTIONS:
            FILENAME: server.js
            RELIES_ON: package.json, client folder
            IS_LIBRARY: False
            LOCATION: root
            EXECUTION_ORDER: 1
            EXECUTION_COMMAND: npm start
            LANGUAGE: JavaScript
            ENV_VARS: N/A
            LIBRARIES: Node.js, Express, MongoDB, React, Passport.js

        - DELIVERABLE: 2
          Solution:
            - Add functionality for displaying a list of all blogs on the homepage
            - Implement pagination for displaying limited number of blogs per page
            - Implement search functionality for searching blogs by keyword
          Dependencies: Node.js, Express, MongoDB, React
          SharedState: N/A
          AdditionalNotes: Uses existing authentication from Deliverable 1
          RUNTIME_INSTRUCTIONS:
            FILENAME: blogList.js
            RELIES_ON: server.js
            IS_LIBRARY: True
            LOCATION: root
            EXECUTION_ORDER: 2
            EXECUTION_COMMAND: N/A
            LANGUAGE: JavaScript
            ENV_VARS: N/A
            LIBRARIES: Node.js, Express, MongoDB, React

        - DELIVERABLE: 3
          Solution:
            - Create functionality to allow users to comment on blogs
            - Implement nested comments for better organization
            - Add ability to upvote/downvote comments
          Dependencies: Node.js, Express, MongoDB, React
          SharedState: N/A
          AdditionalNotes: Uses existing authentication from Deliverable 1
          RUNTIME_INSTRUCTIONS:
            FILENAME: comments.js
            RELIES_ON: blogList.js
            IS_LIBRARY: True
            LOCATION: root
            EXECUTION_ORDER: 3
            EXECUTION_COMMAND: N/A
            LANGUAGE: JavaScript
            ENV_VARS: N/A
            LIBRARIES: Node.js, Express, MongoDB, React

        - DELIVERABLE: 4
          Solution:
            - Add functionality for displaying related blog posts based on keyword/tags
            - Implement sharing functionality on social media platforms
          Dependencies: Node.js, Express, MongoDB, React
          SharedState: N/A
          AdditionalNotes: Uses existing authentication from Deliverable 1
          RUNTIME_INSTRUCTIONS:
            FILENAME: relatedAndSharing.js
            RELIES_ON: comments.js
            IS_LIBRARY: True
            LOCATION: root
            EXECUTION_ORDER: 4
            EXECUTION_COMMAND: N/A
            LANGUAGE: JavaScript
            ENV_VARS: N/A
            LIBRARIES: Node.js, Express, MongoDB, React



        Continue for as many deliverables as required, DO NOT include successive deliverables if they are not imported or connected. 
        Remember, each deliverable does not know about the other, so if imports, file reference or similar is required you need to mention it in the description.
        Remember, each deliverable does not know about the other do not use same filename. 

        EACH filename must be connected via imports or references in the other files, the deliverables don't know about each other so you need to tell them what code to add to connect the other components. If DELIVERABLE: 1 filename is main.py, DELIVERABLE: 2 filename is extraFunctionality.py, then main.py must import extraFunctionality and the same for successive deliverables. 
        The goal here is that the output file of each deliverable comes together into a single project folder with no duplication. 
        Note, the preferred languages are python and bash scripts, but not exclusive such as if building with html, css, etc.
        Note: if the deliverable does not have a EXECUTION_COMMAND just put N/A
        """


        # ----------------- CALL OPEN AI

        print('')
        cprint('Requesting....','white',attrs=['blink'])

        availableResponses   = openaiObject.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}])
        self.currentResponse = availableResponses['choices'][0]['message']['content'].lstrip()
        self.fullDialogue    += prompt + ' \n' + self.currentResponse

        os.system('clear')
        
        # -----------------VALIDATE DELIVERABLES 


        try:
            data = yaml.safe_load(self.currentResponse)
            print(self.currentResponse)
            print('Dict data')
            print(data)
            print('')
            cprint('Does this look correct?', 'yellow',attrs=['bold'])
            print('\n\n')
            cprint('Continue?', 'white',attrs=['blink'])
            input('')
        except:
            print(self.currentResponse)
            cprint('WARNING: Can not verify deliverables match', 'yellow',attrs=['blink'])
            exit()


        # -----------------SAVE

        # Save self.currentResponse to workspace folder as classifiedProblems.txt
        workspace_dir = "workspace"
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)
        with open(os.path.join(workspace_dir, "classifiedProblems.yaml"), "w") as file:
            file.write(self.currentResponse + "\n\n")
        

        # VALIDATE YAML
        passed = validate_yaml('workspace/classifiedProblems.yaml')
        if(not passed):
            cprint('YAML FAILED, continue?', 'red',attrs=['blink'])
            input('')


        # ----------------- SAVE TO ARRAY 

        print('Deliverables are: ')
        print(self.currentResponse)

        # SOLVABLE? 
        if self.currentResponse.lower() == 'false':
            self.problem_state = 'not_solvable_with_code'
        else:
            self.problem_state = 'solvable_with_code'
            self.run_count += 1

        self.state = 'classified'
