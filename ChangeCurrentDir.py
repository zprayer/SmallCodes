"""Show current dir of Python and Change the dir as User input"""
import os
print(os.getcwd())

try:    
    newDir=input("Input the dir you want:")
    os.chdir(newDir)
    print("The current dir has been set to {0}".format(newDir))
except FileNotFoundError as err:
    print("Can not find the path: {0}".format(newDir))
    
        

def resetDir(newDir):
    try:            
        os.chdir(newDir)
        print("The current dir has been set to {0}".format(newDir))
    except FileNotFoundError as err:
        print("Can not find the path: {0}".format(newDir))
