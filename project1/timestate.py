class TimeState:
    """Represents the time in the simulation"""
    def __init__(self,time)->None:
        """Initializes a TimeState and assigns the object its attributes from the parameter"""
        self.time = time
        self.nextMoveTime = 0
        self.nextMove = list()
        self.message = str()

    def currentTime(self)->None:
        """Returns the current time of the TimeState object"""
        return int(self.time)
    def setTime(self,value:int)->None:
        """Sets the time of the TimeState object"""
        self.time = value
    def smallestNextAction(self,val:int)->None:
        """Decides whether or not the input is smaller than the nextMoveTime"""
        if val<self.nextMoveTime:
            self.nextMoveTime = val


