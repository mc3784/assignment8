import InvestmentSimulation as invSim     
import os, errno

def start():
    """
    It handles the flow of the program, calling the function in the InvestmentSimulation class.
    """
    investmentSimulation=invSim.InvestmentSimulation()
    investmentSimulation.processInput()
    removeFileIfExists("results.txt")
    investmentSimulation.runInvestmentSimulation()

def removeFileIfExists(filename):
    """
    Erase the file results.txt if it exists (from a previous run)
    """
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT: 
            raise 

if __name__ == '__main__':
    start()