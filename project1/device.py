from timestate import *
from nextmove import *

class NoMovesLeft(Exception):
    pass


class device():
    """Represents a device"""
    def __init__(self,deviceID: int,propagatesTo: list,timeLag:list)->None:
        """Initializes a device and assigns the object its attributes from the parameter"""
        self.deviceID = int(deviceID)
        self.propagatesTo = propagatesTo
        self.timeLag = timeLag
    def addPropagationDestination(self,destinationDeviceID: int)->None:
        """Takes in an integer and appends the object's list of propagation targets"""
        self.propagatesTo.append(int(destinationDeviceID))
    def addTimeLag(self,deviceTimeLag: int)->None:
        """Takes in an integer and appends the object's list of time lags/increment"""
        self.timeLag.append(int(deviceTimeLag))

    def actionAlert(self,message: str,t:TimeState,listMoves: list)->None:
        """Executes an alert and sends the alert to the device's propagation targets"""
        for m in listMoves.alertedDevices:
            if m[0] == message and int(self.deviceID) in m:
                    return
        if len(self.propagatesTo) > 1:
            for k in range(len(self.propagatesTo)):
                print(f'@{t.currentTime()}: #{self.deviceID} SENT ALERT TO #{self.propagatesTo[k]}: {message}')
                t.smallestNextAction(t.currentTime() + int(min(self.timeLag)))
                listMoves.addMove(NextMove('ALERT',self.propagatesTo[k],message,int(t.currentTime()+self.timeLag[k]),None,'SENT'))
                listMoves.addMove(NextMove('ALERT',self.propagatesTo[k],message,int(t.currentTime()+self.timeLag[k]),self.deviceID,'RECEIVED'))
        elif len(self.propagatesTo) == 0:
            return
        else:
            print(f'@{t.currentTime()}: #{self.deviceID} SENT ALERT TO #{self.propagatesTo[0]}: {message}')
            t.smallestNextAction(t.currentTime() + int(self.timeLag[0]))
            listMoves.addMove(NextMove('ALERT', self.propagatesTo[0], message, int(t.currentTime() + int(self.timeLag[0])),self.deviceID,'RECEIVED'))
            listMoves.addMove(NextMove('ALERT', self.propagatesTo[0], message, int(t.currentTime() + int(self.timeLag[0])),None,'SENT'))

    def actionCancel(self,message: str,t: TimeState,listMoves: list)->None:
        """Executes an cancellation and propagates it to the other devices as per the devices' configuration"""
        if not self.deviceID in listMoves.alertedDevices: listMoves.addAlertedDevice(message,int(self.deviceID))

        if len(self.propagatesTo) > 1:
            for k in range(len(self.propagatesTo)):
                print(f'@{t.currentTime()}: #{self.deviceID} SENT CANCELLATION TO #{self.propagatesTo[k]}: {message}')
                t.smallestNextAction(t.currentTime() + int(min(self.timeLag)))
                listMoves.addMove(NextMove('CANCEL',self.propagatesTo[k],message,int(t.currentTime()+self.timeLag[k]),None,'SENT'))
                listMoves.addMove(NextMove('CANCEL',self.propagatesTo[k],message,int(t.currentTime()+self.timeLag[k]),self.deviceID,'RECEIVED'))
                listMoves.addAlertedDevice(message, self.propagatesTo[k])

        elif len(self.propagatesTo) == 0:
            return
        else:
            print(f'@{t.currentTime()}: #{self.deviceID} SENT CANCELLATION TO #{self.propagatesTo[0]}: {message}')
            t.smallestNextAction(t.currentTime() + int(self.timeLag[0]))
            listMoves.addMove(NextMove('CANCEL', self.propagatesTo[0], message, int(t.currentTime() + int(self.timeLag[0])),self.deviceID,'RECEIVED'))
            listMoves.addMove(NextMove('CANCEL', self.propagatesTo[0], message, int(t.currentTime() + int(self.timeLag[0])),None,'SENT'))

def createDevices(userInput: list)->list:
    """Takes in a list of strings and creates a device everytime a
    string starts with the word 'DEVICE' """
    devices = list()
    for k in userInput:
        if k and k.split()[0] == 'DEVICE':
            devices.append(device(k.split()[1], list(),list()))
    return devices

def assignPropagateAttributes(devices:list,dataInput:list)->None:
    """Takes in a list of devices and a list of strings and will loop through
    the list of strings and look for all strings starting with the word 'PROPAGATE'
    to assign the propagation targets for each device"""
    for k in dataInput:
        if k and k.split()[0] == 'PROPAGATE':
            for m in devices:
                if int(m.deviceID) == int(k.split()[1]):
                    m.addPropagationDestination(k.split()[2])
                    m.addTimeLag(k.split()[3])

def act(listMoves:listOfNextMoves,t:TimeState,devices: list,simLength,firstDeviceCancel:int)->None:
    """Takes in a list of NextMoves and reads the action and calls the corresponding action function"""
    listMoves.removeAlertedDeviceFromListOfMoves()
    listMoves.sortMoves()

    executeMove = listMoves.moveToBeExecuted()
    listMoves.deleteExecutedMove()
    try:
        if executeMove == None:
            raise NoMovesLeft('NoMovesLeft')
        elif executeMove.executeAtTime > t.currentTime():
            t.setTime(executeMove.executeAtTime)
        for k in devices:
            if int(k.deviceID) == int(executeMove.deviceID):
                if executeMove.sentReceive == 'RECEIVED':
                    if executeMove.action =='ALERT':
                        print(f'@{t.currentTime()}: #{executeMove.deviceID} RECEIVED ALERT FROM #{executeMove.fromDevice}: {executeMove.message}')
                    else:
                        print(f'@{t.currentTime()}: #{executeMove.deviceID} RECEIVED CANCELLATION FROM #{executeMove.fromDevice}: {executeMove.message}')
                        if executeMove.deviceID==firstDeviceCancel:
                            raise NoMovesLeft('NoMovesLeft')
                        listMoves.addAlertedDevice(executeMove.message, executeMove.deviceID)
                    return act(listMoves, t, devices,simLength,firstDeviceCancel)

                if executeMove.action == 'CANCEL':
                    k.actionCancel(executeMove.message,t,listMoves)
                    return act(listMoves, t, devices,simLength,firstDeviceCancel)
                else:
                    k.actionAlert(executeMove.message,t,listMoves)
                    return act(listMoves, t, devices,simLength,firstDeviceCancel)
    except:
        print(f'@{simLength}: END')