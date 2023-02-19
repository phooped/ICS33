
class NextMove:
    """Immutable class that stores information about next possible moves"""
    def __init__(self,action,deviceID,message,executeAtTime,fromDevice,sentReceive)->None:
        """Initializes a move and assigns the object its attributes from the parameter"""
        self.deviceID = deviceID
        self.message = message
        self.executeAtTime = int(executeAtTime)
        self.action = action
        self.fromDevice = fromDevice
        self.sentReceive = sentReceive

class listOfNextMoves:
    """Represents a list of the object NextMove"""
    def __init__(self,nextMoves:list)->None:
        """Initializes a listOfNextMoves object and assigns the object its attributes from the parameter"""
        self.nextMoves = nextMoves
        self.alertedDevices = list()
    def addMove(self,move: NextMove)->None:
        """Adds a NextMove object to the object"""
        self.nextMoves.append(move)
    def sortMoves(self)->None:
        """Sorts all the NextMove objects in the object"""
        self.nextMoves.sort(key = lambda x: (x.action),reverse = True)
        self.nextMoves.sort(key = lambda x: (int(x.executeAtTime),x.sentReceive, x.message,int(x.deviceID)))
    def moveToBeExecuted(self)->NextMove:
        """Returns the move that will be executed next"""
        try:
            return self.nextMoves[0]
        except:
            pass
    def deleteExecutedMove(self)->None:
        """Deletes the move that is being executed"""
        try:
            del self.nextMoves[0]
        except:
            pass
    def addAlertedDevice(self,message:str,deviceID:int)->None:
        """Takes in a message and device ID and adds that device to a list of that keeps track of all alerted devices"""
        messages = [item[0] for item in self.alertedDevices]
        if message not in messages:
            self.alertedDevices.append([message])
        for m in self.alertedDevices:
            if m[0] == message and deviceID not in m:
                m.append(deviceID)
    def removeAlertedDeviceFromListOfMoves(self)->None:
        """Removes all NextMove objects from the list object that has already been alerted"""
        for m in self.nextMoves:
            if m.action == 'CANCEL':
                pass
            elif not m.sentReceive=='RECEIVED':
                for k in self.alertedDevices:
                    if k[0] == m.message and m.deviceID in k:
                            del self.nextMoves[self.nextMoves.index(m)]
