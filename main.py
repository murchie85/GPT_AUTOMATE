import os
from termcolor      import colored, cprint 
from art            import *
import problemClassifier
from decomposer import *

class agent_coordinator():
	def __init__(self):
		self.state        = 'not started'
		self.classifier   = problemClassifier.ProblemClassifier()
		self.deliverableStatement = None
		self.no_deliverables      = 0
		self.currentDeliv         = 0
		self.deliverablesArray    = []

	def mainLoop(self):

		if(self.state =='not started'):
			self.classifier.get_requirements()
			if(self.classifier.problem_state == 'solvable_with_code'):
				
				# IMPORT METRICS 
				self.problemStatement     = self.classifier.problemStatement
				self.deliverableStatement = self.classifier.currentResponse 
				self.no_deliverables         = self.classifier.no_deliverables
				self.state = 'decompose'
				
				print('Deliverables : ' + str(self.no_deliverables))
				cprint('Complete! Proceeding to next step', 'white')
				input('')
			else:
				self.state = 'complete'
				cprint('Complete! Problem is not solvable with code unfortunately', 'red')
				input('')
		if(self.state =='decompose'):
			decompose()

os.system('clear')
welcomeMessage=text2art("Welcome")
amuMessage=text2art("Automator V 0.1")
print(welcomeMessage)
print(amuMessage)
coordinator = agent_coordinator()
coordinator.mainLoop()
