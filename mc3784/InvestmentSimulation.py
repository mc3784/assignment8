import numpy as np
import matplotlib.pyplot as plt
import sys

class NotValidInput(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class InvestmentSimulation:
    positions = []
    position_value = []    
    num_trials = 0
    cumu_ret = 0
    daily_ret = 0

    def processInput(self):
        """
        Validate the user input: The first input has to be a List of strictly positive integer numbers, 
        and the second a stricly positive integer number.  
        """
        try:
            positionsInput = raw_input("Write a list of the number of shares to buy in parallel: (not more than 1000)")   
            self.validatePositionList(positionsInput)
            positionsInput = positionsInput[1:-1]
            for pos in positionsInput.strip().split(","):
                self.validateIntegerInput(pos)    
                oneBetAmount = 1000. / int(pos)
                if not float(oneBetAmount).is_integer():
                    erroMessage="The number in the list have to divisors of 1000"
                    raise NotValidInput(erroMessage)                  
                    self.printUsageMessage()
                    sys.exit()
                self.positions.append(int(pos))  
                self.position_value.append(oneBetAmount)              
            num_trialsInput = raw_input("Insert the number of trials")  
            self.validateIntegerInput(num_trialsInput)                   
            self.num_trials = int(num_trialsInput)
            self.cumu_ret = np.zeros((len(self.positions), self.num_trials))
            self.daily_ret = np.zeros((len(self.positions), self.num_trials))
        except KeyboardInterrupt:
            print "\nYou have pressed Control-C: The program is going to terminate" 
            sys.exit()
        except NotValidInput,e:
            print e
            self.printUsageMessage()
            sys.exit()

    def runInvestmentSimulation(self):
        """
        Run the investment simulation for the position in self.positions for num_trials
        """
        for trial in range(self.num_trials):
            self.processInvestment(trial)
        posCounter=0
        for pos in self.positions:
            fileName="histogram_"+str(pos).zfill(4)+"_pos.pdf"
            self.saveIstagramInFile(self.daily_ret[posCounter],fileName)
            dayly_ret_mean=np.mean(self.daily_ret[posCounter])
            dayly_ret_std=np.std(self.daily_ret[posCounter])
            self.saveMeanStdInFile(self.positions[posCounter],dayly_ret_mean,dayly_ret_std)
            posCounter=posCounter+1  

    def validateIntegerInput(self,integerToCheck):
        """
        It raises a NotValidInput if integerToCheck is a string that doesn't rappresent an integer number 
        """
        try:
            if not float(integerToCheck).is_integer():
                erroMessage="One of the input is not an integer: "+integerToCheck
                raise NotValidInput(erroMessage)   
                self.printUsageMessage() 
            if int(integerToCheck)<=0:
                erroMessage="All the input number must be strictly positive integer numbers. This number is not strictly positive: "+integerToCheck
                raise NotValidInput(erroMessage)      
                self.printUsageMessage()       
        except ValueError:
            erroMessage="One of the input is not a number: "+integerToCheck
            raise NotValidInput(erroMessage)  
            self.printUsageMessage() 
            
    def validatePositionList(self,positionsInput):
        """
        It raises a NotValidInput if positionsInput is not a List enclosed in square brackets 
        """        
        if positionsInput[0] != "[" or positionsInput[-1] != "]":
            erroMessage="The input list have to be enclosed in square brackets"
            raise NotValidInput(erroMessage)        
            self.printUsageMessage()
    
    def processInvestment(self,num_trial):
        """
        For each trial it place the investment for all the position in the self.positions list.
        """
        numberOfPosition=0
        try:
            for pos in self.positions:
                oneBetAmount = 1000 / int(pos)
                gain=0.
                for inv in range(int(pos)):
                    gain=gain+oneBetAmount*self.investmentOutcome()
                self.cumu_ret[numberOfPosition][num_trial]=gain
                self.daily_ret[numberOfPosition][num_trial]=float(gain)/1000.-1
                numberOfPosition=numberOfPosition+1
        except Exception,e:
            print e
    
    def saveIstagramInFile(self,daily_ret,fileName):
        """
        It generate an histogram with the data in in daily_ret and it saves it into a file named fileName.
        """
        plt.hist(daily_ret,100,range=[-1,1])
        plt.savefig(fileName)
        plt.clf()
    
    def saveMeanStdInFile(self,position,dayly_mean,dayly_std):
        """
        It saves the mean and the standard deviation for a given position into the results.txt
        """
        lineToWrite="Position="+str(position)+": mean = "+str(dayly_mean)+", std="+str(dayly_std)+"\n"
        with open("results.txt", "a") as myfile:
            myfile.write(lineToWrite)
    
    def investmentOutcome(self):
        """
        It generate randomly the factor to use to generate the outcome of the investment. 51% of the time it's 2 and 49% of the time is 0. 
        """
        if np.random.rand()>=0.51:
            return 2
        else:
            return 0
    def printUsageMessage(self):
        print "USAGE:"
        print "The first input has to be a a list of positive defined integer number enclosed in square brackets, and each number have to be a divisor of 1000"
        print "Example for the first input: [1,10,100,1000]"
        print "The second input has to be a positive defined integer number"
        
