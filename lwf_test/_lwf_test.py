# -*- coding: utf-8 -*-
"""
lwf_test -- Light Weight Function Test

A simple library for unit testing python code

v 0.1a0

Created on Wed Nov 30 11:04:42 2016

@author: Tom Blanchet
"""

from time import time
import traceback
#### GLOBALS ####
TESTS_DISABLED = False
PRINT_KEY_ORDER =  ['test number',\
                    'args',\
                    'kwargs',\
                    'time',\
                    'error',\
                    'expected output',\
                    'true output',\
                    'successes',\
                    'failures',\
                    'errors']
SUCCESS_KEY = "success"
FAILURE_KEY = "failure"
ERROR_KEY = "error"
DISABLED_KEY = "disabled"
CONSOLE_WIDTH = 80
VERBOSE_TESTS = True

#### CLASSES ####
class Timer(object):
    """
    Timer class for timing tests.
    """
    timing = None
    def start(self):
        self.startTime = time()
    
    def stop(self):
        self.timing = self.startTime - time()
        del self.startTime
        
    def getTiming(self):
        return self.timing
        
class _NonTimer(Timer):
    def start(self):
        return
    def stop(self):
        return

class TRHMeta(type):
    """
    Metaclass for TestResultHelper
    """
    def __init__(cls, name, bases, namespace):
        cls.instances = {}
        type.__init__(cls, name, bases, namespace)
    
    def __getitem__(cls, key):
        return cls.instances[key]
    
    def __setitem__(cls, key, value):
        cls.instances[key] = value
    
    def __iter__(cls):
        for k in cls.instances:
            yield k
    
    def getOutcomeTotals(cls):
        """
        Get the outcome totals for all tests
        """
        ret = {'successes': 0, 'failures': 0, 'errors': 0}
        for func in cls:
            for key in ret:
                ret[key] += len(cls[func].__getattribute__(key))
        return ret
        
    def getTotalTests(cls):
        """
        Get the total number of tests performed.
        """
        ret = 0
        outTotals = cls.getOutcomeTotals()
        for v in outTotals.values():
            ret += v
        return ret
        
        
  
class TestResultHelper(object, metaclass = TRHMeta):
    """
    Helper for managing test results.
    
    Usage:
        #For managing all function tests, simply use the class
        print("Total number of tests:", TestResultHelper.getTotalTests())
        
        #Will print (in some order):
        #>>> successes : <total successes for all tests>
        #>>> failures : <total failures for all tests>
        #>>> errors : <total errors for all tests>
        for k, v in TestResultHelper.getOutcomeTotals().items():
            print(k, ":", v)
        
        #Gets the TestResultsHelper instance for the named function. 
        #Can also use TestResultsHelper.getInstanceForFunc(myFunction)
        testHelper = TestResultsHelper['myFunction']
        
        #The instance methods are similar to the Class methods, 
        #but just for the given function's tests.
        print("Total number of tests for myFunction:", testHelper.getTotalTests())
        
        #Will print (in some order):
        #>>> successes : <total successes for function tests>
        #>>> failures : <total failures for function tests>
        #>>> errors : <total errors for function tests>
        for k, v in testHelper.getOutcomeTotals().items():
            print(k, ":", v)
    """
    def __init__(self, func):
        funcName = self._initFuncName(func)
        TestResultHelper[funcName] = self
        self.successes = []
        self.failures = []
        self.errors = []
        self.funcName = funcName
        self._makeInstanceMethods()
    
    @staticmethod
    def _initFuncName(func):
        funcName = func.__name__
        suff = ""
        count = 0
        while(funcName + suff in TestResultHelper.instances):
            count += 1
            suff = str(count)
        funcName += suff
        return funcName
        
    def _makeInstanceMethods(self):
        for name in self.__dir__():
            if(name[:6] == "_inst_"):
                method = self.__getattribute__(name)
                self.__setattr__(name[6:], method)
    
    def _inst_getOutcomeTotals(self):
        """
        Get the outcome totals for all tests for this function.
        """
        ret = {'successes': 0, 'failures': 0, 'errors': 0}
        for key in ret:
            ret[key] = len(self.__getattribute__(key))
        return ret
    
    def _inst_getTotalTests(self):
        """
        Get the total number of tests performed for the function.
        """
        ret = 0
        outTotals = self.getOutcomeTotals()
        for v in outTotals.values():
            ret += v
        return ret
        
    @classmethod
    def getInstanceForFunc(cls, func):
        """
        Get the instance of the associated function.
        """
        return cls[func.__name__]
    

#### HELPER FUNCTIONS ####

###Private
def _bindTesterContext(tester, func):
    """
    Binds the tester to the function 
    and modifies the tester attributes to
    work better in context.
    """
    tester.__name__ = "{funcName}.Tester".format(funcName = func.__name__)
    func.Tester = tester
    
def _tryToBundleTiming(resBundle, timer):
    """
    Attempts assign the timing in timer to resBundle['time']
    """
    time = timer.getTiming()
    if(time != None):
        resBundle['time'] = timer.getTiming()
            
def _printSortKey(key):
    """
    Function to pass the key keyword in sorted
    when sorting test result dictionary keys for printing.
    """
    global PRINT_KEY_ORDER
    if(key in PRINT_KEY_ORDER):
        return PRINT_KEY_ORDER.index(key)
    else:
        return len(PRINT_KEY_ORDER) + 1
  
def _printTestResults(funcName, testResult, resBundle):
    """
    Prints the results of a single test.
    """
    testResult = str(testResult)
    testNumber = resBundle['test number']
    print("Result for {funcName} test # {testNumber}:\n::::::{res}::::::".format(\
                 funcName = funcName, testNumber = testNumber,\
                 res = testResult.upper()))
    print("    Details:")
    for k in sorted(resBundle.keys(), key = _printSortKey):
        if(k == 'tb_str'):
            print("    ",_reform_tb_str(resBundle[k], frontPad = 8), sep="")
        elif(k != 'test number'):
            print("    ", k.capitalize(), ": ", repr(resBundle[k]), sep="")
    print()
    
def _reform_tb_str(tb_str, frontPad = 0):
    global CONSOLE_WIDTH
    lineMax = CONSOLE_WIDTH - frontPad
    if(lineMax<0): #Fail safe
        return tb_str
    split_tb_str = tb_str.split('\n')
    new_splits = []
    for tb_line in split_tb_str:
        line_indent = len(tb_line) - len(tb_line.lstrip(" "))
        indent_str = " " * line_indent
        lineStart = line_indent
        lineEnd = lineMax
        curLineLen = len(tb_line)
        while(lineStart<curLineLen):
            new_splits.append(indent_str + tb_line[lineStart:lineEnd])
            lineStart = lineEnd
            lineEnd += lineMax - line_indent
    return ('\n' + ' ' * frontPad).join(new_splits)
        
###Public
def disableTests():
    """
    Disable test functionality.
    """
    global TESTS_DISABLED
    TESTS_DISABLED = True
    
def enableTests():
    """
    Enable test functionality. (Enabled by default)
    """
    global TESTS_DISABLED
    TESTS_DISABLED = False
    
def disableVerboseTests():
    """
    Disable printing for each test.
    """
    global VERBOSE_TESTS
    VERBOSE_TESTS = False
    
def enableVerboseTests():
    """
    Enable printing for each test. (Enabled by default)
    """
    global VERBOSE_TESTS
    VERBOSE_TESTS = True
    
def printFinalResults(verbose = False):
    """
    Prints the final results of testing (so far)
    
    If verbose is True, will also (re)print each of the individual
    test results.
    """
    
    if(verbose):
        for funcName in TestResultHelper:
            testerHelperIns = TestResultHelper[funcName]
            print("======= Successes =======")
            for s in testerHelperIns.successes:
                _printTestResults(funcName, "success", s)
            print("======= Failures =======")
            for f in testerHelperIns.failures:
                _printTestResults(funcName, "failure", f)
            print("======= Errors =======")
            for e in testerHelperIns.errors:
                _printTestResults(funcName, "error", e)
    
    outcomes = TestResultHelper.getOutcomeTotals()
    total = TestResultHelper.getTotalTests()
    print("======= Final Test Summary =======")
    print("Total Tests:", total)
    for outcomeKey in sorted(outcomes.keys(), key = _printSortKey):
        print(outcomeKey.capitalize(), outcomes[outcomeKey], sep = ": ")
        
        
#### WRAPPERS #### 
def makeTester(comp = lambda a, b: a == b,\
               catchErrors = (Exception,), timer = None):
    """
    Binds a Tester attribute to the wrapped function.
    
    Wrapper Factory Arguements:
        
        comp :: (output, output) -> boolean
            A comparison function for two function outputs
            defaults to normal comparison
            
        catchErrors :: tuple(Exception) | Exception
            A tuple of Exceptions to acknowledge and catch.
            May also be a single Exception (as demonstrated below)
            
        timer :: None | Timer
            An optional Timer object. Just before calling the function,
            timer.start() will be called. Then, after the function returns,
            timer.stop() will be called. The time will be retrieved via
            timer.getTiming(). 
    
    func.Tester :: str
        The Tester attribute that will be bound to the wrapped function.
        
        The Tester attribute will return either "success", "failure", or "error"
        according to the test result unless tests are disabled. 
        (In which case, the Tester attribute will return "disabled")
        
        If testing is not disabled, the results will be recorded in
        the TestResultsHelper class as a side-effect. 
    
    Usage:
        disableVerboseTests() #Will not print individual outcomes this way
        
        @makeTester(catchErrors = ZeroDivisionError)
        def myFunction(a, b):
            return a/b
        
        print(myFunction.Tester(5, 15, 3)) #Will return "success"
        print(myFunction.Tester(1, 4, 2))  #Will return "failure"
        print(myFunction.Tester(20, 4, 0)) #Will return "error"
        try:
            #This try block will raise an error that will not be caught
            #and the test will not be registered in TestResultsHelper
            
            print(myFunction.Tester(3, "hi", "there"))
            
        except TypeError as te: 
            print("fatal error:", te)
            #raise
            
            #Ideally, you would want to raise these errors
            #so that testing stops. 
        
        #Gets the TestResultsHelper instance for the named function. 
        #Can also use TestResultsHelper.getInstanceForFunc(myFunction)
        
        testHelper = TestResultHelper['myFunction']
        
        #Will print "3", ignoring the unexpected error
        print("Total number of tests:", testHelper.getTotalTests())
        
        #Will print (in some order):
        #>>> successes : 1
        #>>> failures : 1
        #>>> errors : 1
        for k, v in testHelper.getOutcomeTotals().items():
            print(k, ":", v)
        
    """
    if timer == None:
        timer = _NonTimer()
    def wrapper(func):
        
        testHelper = TestResultHelper(func)
        testNumber = 0
        
        def tester(output=None, *args, **kwargs):
            
            global SUCCESS_KEY
            global FAILURE_KEY
            global ERROR_KEY
            global DISABLED_KEY
            global VERBOSE_TESTS
            
            verbose = VERBOSE_TESTS
            
            global TESTS_DISABLED
            if(TESTS_DISABLED):
                return DISABLED_KEY
                
            nonlocal testNumber
            nonlocal testHelper
            
            testNumber += 1
            resBundle = {'args': args,\
                         'kwargs': kwargs,\
                         'expected output': output,\
                         'test number': testNumber
                         }
            ret = None
                
            timer.start()
            try:
                funcOut = func(*args, **kwargs)
            except catchErrors as e:
                timer.stop()
                ret = ERROR_KEY
                resBundle['error'] = e
                resBundle['tb_str'] = traceback.format_exc()
                _tryToBundleTiming(resBundle, timer)
                
                testHelper.errors.append(resBundle)    
            else:
                timer.stop()
                resBundle['true output'] = funcOut
                _tryToBundleTiming(resBundle, timer)
                
                if(comp(funcOut, output)):
                    ret = SUCCESS_KEY
                    testHelper.successes.append(resBundle)
                else:
                    ret = FAILURE_KEY
                    testHelper.failures.append(resBundle)
            finally:
                try:
                    timer.stop()
                except:
                    pass
                    
            if(verbose):
                _printTestResults(func.__name__, ret, resBundle)
            return ret
        
        _bindTesterContext(tester, func)
        
        return func
        
    return wrapper
    