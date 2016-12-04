# -*- coding: utf-8 -*-
"""
Tests for LWFTest

Created on Thu Dec  1 16:27:59 2016

@author: Tom Blanchet
"""
from functools import wraps
#import sys
from importlib import reload

def TestError(Exception):
    pass

ALL_TESTS = []
def testDec(testFunc):
    global ALL_TESTS
    @wraps(testFunc)
    def testWrapper(*args, **kwargs):
        _cleanTests()
        try:
            return True, testFunc(*args, **kwargs)
        except Exception as e:
            return False, e
    ALL_TESTS.append(testWrapper)
    return testWrapper

def _cleanTests():
    import lwf_test
    reload(lwf_test._lwf_test)
    reload(lwf_test)
    
@testDec
def importTest():
    import lwf_test
    print(dir(lwf_test))
    from lwf_test import TestResultHelper
    from lwf_test import makeTester

@testDec
def test0():
    
    from lwf_test import makeTester, printFinalResults,\
                    SUCCESS_KEY, FAILURE_KEY, ERROR_KEY, TestResultHelper
    
    @makeTester()
    def nothing():
        return
    
    @makeTester()
    def add(a, b):
        return a + b
        
    lambda_add = makeTester()(lambda a, b: a + b)
    
    class simpleObject(object):
        number = 0
        total = 0
        def __init__(self):
            simpleObject.total += 1
            self.index = simpleObject.total
        @makeTester()
        def doSomething(self):
            simpleObject.number += 1
            return str(self.index) + "hi" + str(simpleObject.number)
    
    assert nothing.Tester()         == SUCCESS_KEY
    assert nothing.Tester(None)     == SUCCESS_KEY
    assert nothing.Tester(None, 2)  == ERROR_KEY
    assert add.Tester()             == ERROR_KEY
    assert add.Tester(5, 1, 2)      == FAILURE_KEY
    assert add.Tester(5, 2, 3)      == SUCCESS_KEY
    assert lambda_add.Tester(5, 1, 2)      == FAILURE_KEY
    assert lambda_add.Tester(5, 2, 3)      == SUCCESS_KEY
    
    objA = simpleObject()
    objB = simpleObject()
    
    assert simpleObject.doSomething.Tester("GIVE ERROR") == ERROR_KEY
    
    assert simpleObject.doSomething.Tester("1hi1", objA) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("1hi2", objA) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("2hi3", objB) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("2hi4", objB) == SUCCESS_KEY
    
    assert objA.doSomething() == "1hi5"
    
    printFinalResults()
    
@testDec
def testMakeTesterAlphaDoc():
        from lwf_test import makeTester, TestResultHelper, disableVerboseTests
        
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
        
@testDec
def disableTest():
    from lwf_test import makeTester, printFinalResults, DISABLED_KEY,\
                        disableTests, enableTests,\
                        SUCCESS_KEY, FAILURE_KEY, ERROR_KEY
    
    disableTests()
    
    @makeTester()
    def nothing():
        return
    
    @makeTester()
    def add(a, b):
        return a + b
        
    lambda_add = makeTester()(lambda a, b: a + b)
    
    class simpleObject(object):
        number = 0
        total = 0
        def __init__(self):
            simpleObject.total += 1
            self.index = simpleObject.total
        @makeTester()
        def doSomething(self):
            simpleObject.number += 1
            return str(self.index) + "hi" + str(simpleObject.number)
    
    assert nothing.Tester()         == DISABLED_KEY
    assert nothing.Tester(None)     == DISABLED_KEY
    assert nothing.Tester(None, 2)  == DISABLED_KEY
    assert add.Tester()             == DISABLED_KEY
    assert add.Tester(5, 1, 2)      == DISABLED_KEY
    assert add.Tester(5, 2, 3)      == DISABLED_KEY
    assert lambda_add.Tester(5, 1, 2)      == DISABLED_KEY
    assert lambda_add.Tester(5, 2, 3)      == DISABLED_KEY
    
    objA = simpleObject()
    objB = simpleObject()
    
    assert simpleObject.doSomething.Tester("GIVE ERROR") == DISABLED_KEY
    
    assert simpleObject.doSomething.Tester("1hi1", objA) == DISABLED_KEY
    assert simpleObject.doSomething.Tester("1hi2", objA) == DISABLED_KEY
    assert simpleObject.doSomething.Tester("2hi3", objB) == DISABLED_KEY
    assert simpleObject.doSomething.Tester("2hi4", objB) == DISABLED_KEY
    
    assert objA.doSomething() == "1hi1"
    
    printFinalResults()
    
    enableTests()
    
    assert nothing.Tester()         == SUCCESS_KEY
    assert nothing.Tester(None)     == SUCCESS_KEY
    assert nothing.Tester(None, 2)  == ERROR_KEY
    assert add.Tester()             == ERROR_KEY
    assert add.Tester(5, 1, 2)      == FAILURE_KEY
    assert add.Tester(5, 2, 3)      == SUCCESS_KEY
    assert lambda_add.Tester(5, 1, 2)      == FAILURE_KEY
    assert lambda_add.Tester(5, 2, 3)      == SUCCESS_KEY
    
    assert simpleObject.doSomething.Tester("GIVE ERROR") == ERROR_KEY
    
    assert simpleObject.doSomething.Tester("1hi2", objA) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("1hi3", objA) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("2hi4", objB) == SUCCESS_KEY
    assert simpleObject.doSomething.Tester("2hi5", objB) == SUCCESS_KEY
    
    assert objA.doSomething() == "1hi6"
    
    printFinalResults()
    
def main():
    for test in ALL_TESTS:
        print("Running", test.__name__)
        testRes = test()
        
        try:
            if not testRes[0]:
                raise testRes[1]
        finally:
            print("Result:", testRes)
        print()
        
    print("All Tests Passed!")
    
if __name__ == "__main__":
    main()
                
            
    