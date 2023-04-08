# GPT Automator 



1. Problem classifier 
2. High level code planner breaks problem down into smallest deliverable components as instructions for the next step.
3. Code Generator Decomposition Agent:  Called for each smallest deliverable increment.
If under 4000 tokens create, if more, call agent with instructions for 4k token piecemeal delivery.
Must include Code only, at end of code block, should include a operation instruction different kind of markup code we will agree, something like.
RUN=PYTHON,FILENAME=main.py,SAVE_LOCATION=src
4. 4EyesCheck Agent: Iterates all the produced instructions from GPT, checks if it can be parsed properly by automation harness. Also ensures runtime instructions are correct. 
5. File Creator Automation: Saves files in the correct place.
6. Runner: Executes code based upon step3.
7. Automated Output Capture
8 GPT Debugger agent. Setup in the same way where we have a language which says what file to change/replace.
9. Repeat - once no errors, human checks, Provides feedback into original prompt and repeats. 


## implementation 

Create a class for each agent:

ProblemClassifier
HighLevelCodePlanner
CodeGeneratorDecompositionAgent
FourEyesCheckAgent
FileCreatorAutomation
Runner
AutomatedOutputCapture
GPTDebuggerAgent
Create an orchestrator class ProjectCreator that initializes and calls these agent classes in the appropriate order.




















# --------LEGACY


SET UP MULTIPLE GPT AGENTS WITH DIFFERENT INITIAL SYSTEM PROMPTS INCLUDING:  


- GPT Problem classifier
- GPT Code Generator
- GPT Code RunTime advisor (produces parsable tokens i.e. RUN_MAIN.PY RUN_START.SH etc)
- GPT Code Directory Checker (stiched prompts to ensure all files, code in the right place in the folder)
- Automation Harness Runner - Runs the main.py or instructions given by RunTime advisor
- Automation Harness OutPut Capture - captures terminal, log outputs.
- GPT debugger - Reviews logs/errors and enriches description with provided high level solutions.
	
	-- LOOP REPEATS with high level solutions passed back into problem classifier 


## MORE INFO:

1. USER inputs `problem statement`
2. GPT Problem classifier  Agent kicks in, categorises it into: 
```shell
Can solve with code || Can Not solve with code. 
```
3. If Can Not - produce Business plan only
4. If Can: move to next step



# GPT Automator

Set up multiple GPT agents with different initial system prompts:

1. GPT Problem Classifier
2. GPT Code Generator
3. GPT Code RunTime Advisor
4. GPT Code Directory Checker
5. Automation Harness Runner
6. Automation Harness Output Capture
7. GPT Debugger

User inputs the problem statement:

Collect the user's problem statement and pass it to the GPT Problem Classifier agent

## Problem classification:

GPT Problem Classifier agent processes the problem statement and categorizes it into "Can solve with code" or "Cannot solve with code"

### Handle "Cannot solve with code" cases:

If the problem statement falls into the "Cannot solve with code" category, generate a business plan or other relevant output

### Handle "Can solve with code" cases:

1. Pass the problem statement to the GPT Code Generator agent
2. Generate the necessary code using the GPT Code Generator agent
3. Pass the generated code to the GPT Code RunTime Advisor agent, which produces parsable tokens (e.g., RUN_MAIN.PY, RUN_START.SH)
4. Use the GPT Code Directory Checker agent to ensure all files and code are in the right place in the folder
5. Execute the main.py or instructions given by the GPT Code RunTime Advisor using the Automation Harness Runner
6. Capture terminal and log outputs using the Automation Harness Output Capture agent

## Debugging and iterative improvement:

1. Pass the captured outputs to the GPT Debugger agent, which reviews logs/errors and enriches the description with high-level solutions
2. Loop and repeat the process with the high-level solutions passed back into the GPT Problem Classifier agent for further refinement

## Optimize and maintain the system:

- Continuously analyze the performance metrics to identify bottlenecks or inefficiencies in the process
- Fine-tune the prompts, testing methodology, or other aspects of the system to improve code quality and system performance
- Regularly monitor the system's performance and address any emerging issues
- Update the system as needed to incorporate new GPT models, API changes, or other relevant updates

## Document the system and create user guides:

- Document the architecture, configuration, and usage of the system for future reference
- Develop user guides or tutorials to help users interact with and utilize the GPT Automator

## Integrate the solution with existing systems:

- Develop APIs or interfaces to connect the GPT Automator with existing code repositories, CI/CD pipelines, or other relevant systems
