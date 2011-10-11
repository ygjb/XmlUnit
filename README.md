
XmlUnit is a basic library for emitting JUnit style XML files.  This is useful for generating results for easy into tools like Jenkins.

The library is designed to be easy to use:

import sys, random
from XmlUnit import XmlUnit 

report = XmlUnit()

testsuite = report.createSuite("foo suite", "optional machine name")

testsuite.start() 

case = testsuite.createCase("Bar Test", "optional class name")

case.start()

try:
  # do test stuff
  i = random.randint(1,3)
  if i==1:
   passed = True
  elif i==2:
   passed = False
  else:
   raise Exception("uh-oh")
  
  if passed == True:
    case.succeed()
  else:
    case.fail("test failure", "The test failed!")
except Exception, e:
  case.error("exception", "Error %s" % e)

# case.(succeed|error|skip|fail|custom) all implicitly finish the case, and no further action is required.

# you don't have to finish a suite before you start another
# and both XmlUnit.createSuite() and TestSuite.createCase() 
# have start() methods that return the object, so you can do this:
suite2 = report.createSuite("Boo Suite").start()
case = suite2.createCase("Bar Test 2").start()
case.skip("skipping test", "Not today...")

testsuite.finish()
suite2.finish()
#when you are done with your tests, write the report somewhere.
report.write(sys.stdout)

More documentation will be coming, and it will be packaged properly as well.




