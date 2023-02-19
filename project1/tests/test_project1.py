import contextlib
import io
import unittest
from project1 import *
from device import *
from timestate import *

class Tester(unittest.TestCase):
    def test_file_not_found(self):
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            readFile(Path("incorrect directory"))
        self.assertTrue(printedStatement.getvalue(),'FILE NOT FOUND')
    def test_createDevices_correct_number_of_devices(self):
        filteredTxt = ['DEVICE 1','DEVICE 13','DEVICE 129','PROPAGATE 1 3 200']
        devices = createDevices(filteredTxt)
        self.assertTrue(len(devices)==3,True)
    def test_createDevices_correct_deviceID(self):
        filteredTxt = ['DEVICE 1', 'DEVICE 13', 'DEVICE 129', 'PROPAGATE 1 3 200']
        devices = createDevices(filteredTxt)
        self.assertTrue(int(devices[0].deviceID) == 1 and int(devices[1].deviceID) == 13 and int(devices[2].deviceID) == 129, True)
    def test_device_addPropagationDestination_single_device(self):
        newDevice = device(1,list(),200)
        newDevice.addPropagationDestination(3)
        self.assertTrue(newDevice.propagatesTo == [3], True)
    def test_device_addPropagationDestination_multiple_device(self):
        newDevice = device(1, list(), 200)
        newDevice.addPropagationDestination(3)
        newDevice.addPropagationDestination(5)
        newDevice.addPropagationDestination(139)
        self.assertTrue(newDevice.propagatesTo == [3,5,139], True)

    def test_assignPropagateAttributes_single_device(self):
        sampleListOfDevices = [device('1',list(),[500]),device(2,list(),[900])]
        sampleListOfString = ['PROPAGATE 1 2 1000','PROPAGATE 2 1 300']
        assignPropagateAttributes(sampleListOfDevices,sampleListOfString)
        device1CorrectTarget = ([2]==sampleListOfDevices[0].propagatesTo)
        device2CorrectTarget = ([1]==sampleListOfDevices[1].propagatesTo)
        self.assertTrue(device1CorrectTarget and device2CorrectTarget, True)

    def test_assignPropagateAttributes_propagates_to_multiple_device(self):
        sampleListOfDevices = [device('1', list(), [500]), device(2, list(), [900])]
        sampleListOfString = ['PROPAGATE 1 2 1000', 'PROPAGATE 2 1 300','PROPAGATE 1 4 230', 'PROPAGATE 1 9 300']
        assignPropagateAttributes(sampleListOfDevices, sampleListOfString)
        device1CorrectTarget = ([2,4,9] == sampleListOfDevices[0].propagatesTo)
        device2CorrectTarget = ([1] == sampleListOfDevices[1].propagatesTo)
        self.assertTrue(device1CorrectTarget and device2CorrectTarget, True)

    def test_filterFileActionsOnly_correct_output(self):
        sampleInput = ['CANCEL 1 Trouble 2200','ALERT 1 Trouble 0','BAD','# These are the four','PROPAGATE 4 1 1000','DEVICE 4']
        expectedOutput = ['CANCEL 1 Trouble 2200','ALERT 1 Trouble 0']
        filteredInput = filterFileActionsOnly(sampleInput)
        self.assertTrue(expectedOutput == filteredInput, True)

    def test_getSimulationLength_correct_output(self):
        sampleInput = ['CANCEL 1 Trouble 2200','ALERT 1 Trouble 0','BAD','# These are the four','LENGTH 2','PROPAGATE 4 1 1000','DEVICE 4']
        expectedOutput = 120000
        processedInput = getSimulationLength(sampleInput)
        self.assertTrue(expectedOutput == processedInput, True)

    def test_getSimulationLength_negative_input(self):
        sampleInput = ['CANCEL 1 Trouble 2200', 'ALERT 1 Trouble 0', 'BAD', '# These are the four',
                       'LENGTH -2', 'PROPAGATE 4 1 1000', 'DEVICE 4']
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            getSimulationLength(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip()=='Error: Simulation length cannot be negative',True)


    def test_startSimulation_correct_prints(self):
        sampleInput =['LENGTH 2','DEVICE 1','DEVICE 2','DEVICE 3','DEVICE 4','PROPAGATE 1 2 750','PROPAGATE 2 3 1250','PROPAGATE 3 4 500','PROPAGATE 4 1 1000','ALERT 1 Trouble 0','CANCEL 1 Trouble 2200']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@750: #2 SENT ALERT TO #3: Trouble
@2000: #3 RECEIVED ALERT FROM #2: Trouble
@2000: #3 SENT ALERT TO #4: Trouble
@2200: #1 SENT CANCELLATION TO #2: Trouble
@2500: #4 RECEIVED ALERT FROM #3: Trouble
@2500: #4 SENT ALERT TO #1: Trouble
@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble
@2950: #2 SENT CANCELLATION TO #3: Trouble
@3500: #1 RECEIVED ALERT FROM #4: Trouble
@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble
@4200: #3 SENT CANCELLATION TO #4: Trouble
@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble
@4700: #4 SENT CANCELLATION TO #1: Trouble
@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip()==expectedOutput,True)

    def test_startSimulation_correct_prints_propagate_first_to_smaller_id(self):
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2', 'DEVICE 3','DEVICE 4',
                       'PROPAGATE 1 2 750', 'PROPAGATE 1 3 1250', 'PROPAGATE 1 4 500',
                        'ALERT 1 Trouble 0']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: Trouble
@0: #1 SENT ALERT TO #3: Trouble
@0: #1 SENT ALERT TO #4: Trouble
@500: #4 RECEIVED ALERT FROM #1: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@1250: #3 RECEIVED ALERT FROM #1: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip()==expectedOutput,True)

    def test_startSimulation_correct_prints_multiple_initiate_same_message_different_device(self):
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2', 'DEVICE 3', 'DEVICE 4',
                       'PROPAGATE 1 2 750', 'PROPAGATE 3 4 750',
                       'ALERT 1 Trouble 0','ALERT 3 Trouble 0']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: Trouble
@0: #3 SENT ALERT TO #4: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@750: #4 RECEIVED ALERT FROM #3: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip() == expectedOutput,True)

    def test_startSimulation_correct_prints_multiple_initiate_same_device_different_message(self):
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2','PROPAGATE 1 2 750',
                       'ALERT 1 Trouble 0', 'ALERT 1 AAAAAAAA 0']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: AAAAAAAA
@0: #1 SENT ALERT TO #2: Trouble
@750: #2 RECEIVED ALERT FROM #1: AAAAAAAA
@750: #2 RECEIVED ALERT FROM #1: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip() == expectedOutput, True)

    def test_startSimulation_correct_prints_cancellation_first(self):
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2', 'PROPAGATE 1 2 750',
                       'ALERT 1 Trouble 0', 'CANCEL 1 Trouble 0']
        expectedOutput = '''@0: #1 SENT CANCELLATION TO #2: Trouble
@750: #2 RECEIVED CANCELLATION FROM #1: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip() == expectedOutput, True)

    def test_startSimulation_correct_prints_two_device_same_time_smaller_ID_first(self):
        """Tests the rule:'If 2 devices receive a message at the same time,
        the device with the smaller device ID receives & processes all of
        its messages before the next device does.'"""
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2', 'DEVICE 3','PROPAGATE 1 2 750','PROPAGATE 1 3 750',
                       'ALERT 1 Trouble 0']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: Trouble
@0: #1 SENT ALERT TO #3: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@750: #3 RECEIVED ALERT FROM #1: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip() == expectedOutput, True)

    def test_startSimulation_correct_prints_multiple_cancellation(self):
        sampleInput = ['LENGTH 2', 'DEVICE 1', 'DEVICE 2','DEVICE 3','DEVICE 4',
                       'PROPAGATE 1 2 750','PROPAGATE 1 3 450','PROPAGATE 2 4 1000','PROPAGATE 3 4 1000',
                       'ALERT 1 Trouble 0', 'CANCEL 1 Trouble 400']
        expectedOutput = '''@0: #1 SENT ALERT TO #2: Trouble
@0: #1 SENT ALERT TO #3: Trouble
@400: #1 SENT CANCELLATION TO #2: Trouble
@400: #1 SENT CANCELLATION TO #3: Trouble
@450: #3 RECEIVED ALERT FROM #1: Trouble
@750: #2 RECEIVED ALERT FROM #1: Trouble
@850: #3 RECEIVED CANCELLATION FROM #1: Trouble
@850: #3 SENT CANCELLATION TO #4: Trouble
@1150: #2 RECEIVED CANCELLATION FROM #1: Trouble
@1150: #2 SENT CANCELLATION TO #4: Trouble
@1850: #4 RECEIVED CANCELLATION FROM #3: Trouble
@2150: #4 RECEIVED CANCELLATION FROM #2: Trouble
@120000: END'''
        with contextlib.redirect_stdout(io.StringIO()) as printedStatement:
            startSimulation(sampleInput)
        self.assertTrue(printedStatement.getvalue().strip() == expectedOutput, True)
    def test_readFile(self):
        lst = readFile('test')
        expectedOutput = ['t','e','s','t']
        self.assertTrue(lst == expectedOutput, True)



if __name__ == "__main__":
    unittest.main()
