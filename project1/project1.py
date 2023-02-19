from device import *
import timestate
from pathlib import Path
from nextmove import *


KEYWORDSTIME = {'ALERT', 'CANCEL'}


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    data = openFile(input_file_path)
    startSimulation(data)
def openFile(filePath)->list:
    """Returns a list of strings for each line of a text file when inputed a file path"""
    with open(filePath) as file:
        return readFile(file)
def readFile(file)->list:
    """Takes in a file object and returns a list that holds the contents of the file"""
    returnList = []
    try:
        for k in file:
            returnList.append(k.strip())
        return returnList
    except:
        print('FILE NOT FOUND')


def filterFileActionsOnly(dataInput:list)->list:
    """Takes in a list of strings and filters the strings that have action keywords,
    appending them to a new list and returning that list"""
    actions = list()
    for k in dataInput:
        if k and k.split()[0] in KEYWORDSTIME:
            actions.append(k)
    return actions

def getSimulationLength(dataInput: list)->int:
    """Takes in a list of strings and finds the first string that starts
    with 'LENGTH' and calculates and returns the simulation run time"""
    for m in dataInput:
        if m and m.split()[0] == 'LENGTH':
            if int(m.split()[1])>=0:
                return (int(m.split()[1])*60*1000)
            else:
                print('Error: Simulation length cannot be negative')
                return

def getFirstDeviceCancel(dataInput: list)->int:
    """Takes in a list of strings and finds the first string that starts
        with 'CANCEL' and returns the associated device ID"""
    for m in dataInput:
        if m and m.split()[0] == 'CANCEL':
            return (int(m.split()[1]))
    return


def startSimulation(dataInput: list)->None:
    """Starts the simulation"""
    t = timestate.TimeState(0)

    devices = createDevices(dataInput)
    assignPropagateAttributes(devices,dataInput)

    actions = filterFileActionsOnly(dataInput)

    listMoves = listOfNextMoves(list())
    for k in actions:
        listMoves.addMove(NextMove(k.split()[0],k.split()[1],k.split()[2],k.split()[3],None,'SENT'))

    simLength = getSimulationLength(dataInput)
    firstDeviceCancel=getFirstDeviceCancel(dataInput)

    t.nextMoveTime = max([int(sub.split()[3]) for sub in actions if len(sub.split()) > 1])
    act(listMoves, t, devices,simLength,firstDeviceCancel)



if __name__ == '__main__':
    main()
