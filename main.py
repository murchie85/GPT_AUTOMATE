import os
from termcolor      import colored, cprint 
from art            import *
import problemClassifier
from decomposer import *
from getToken import *

class agent_coordinator():
	def __init__(self):
		self.state        = 'not started'
		self.classifier   = problemClassifier.ProblemClassifier()
		self.deliverableStatement = None
		self.no_deliverables      = 0
		self.currentDeliv         = 0
		self.deliverablesArray    = []
		self.openaiObject         = None

	def mainLoop(self):

		self.openaiObject = getOpenAPIKey()

		if(self.state =='not started'):
			self.classifier.get_requirements(self.openaiObject)
			if(self.classifier.problem_state == 'solvable_with_code'):
				
				# IMPORT METRICS 
				self.problemStatement     = self.classifier.problemStatement
				self.deliverableStatement = self.classifier.currentResponse 
				self.no_deliverables         = self.classifier.no_deliverables
				self.state = 'decompose'
				
				print('Deliverables : ' + str(self.no_deliverables))
				cprint('Complete! press any key to proceed to the next step', 'white')
				input('')
			else:
				self.state = 'complete'
				cprint('Complete! Problem is not solvable with code unfortunately', 'red')
				input('')
		if(self.state =='decompose'):
			decompose(self.openaiObject)

os.system('clear')
welcomeMessage=text2art("Welcome")
amuMessage=text2art("Automator V 0.1")
print(welcomeMessage)
print(amuMessage)
coordinator = agent_coordinator()
coordinator.mainLoop()
