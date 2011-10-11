

from XmlUnit import XmlUnit

report = XmlUnit()

suite = report.createSuite("test1")
suite.start()

case = suite.createCase("test case 1").start()
case.succeed()

case = suite.createCase("test case 2").start()
case.error("general error", "This test errored out")

case = suite.createCase("testcase 3").start()
case.fail("general failure", "This is a failed test case")

case = suite.createCase("Final case").start()
case.succeed()


suite.finish()

suite = report.createSuite("test2")
suite.start()

case = suite.createCase("bravo test case 1")
case.start()
case.error("general error", "This test errored out")

suite.finish()

file = open("test.xml", "w")
report.write(file)
file.close()