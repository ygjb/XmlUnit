from datetime import datetime
from xml.dom.minidom import Document

class XmlUnit():
	
	def __init__(self):
		self.testsuites = []
	
	def createSuite(self, name, hostname = "localhost"):
		suite = TestSuite(name, hostname)
		self.testsuites.append(suite)
		return suite
	
	def finish(self):
		for suite in self.testsuites:
			if suite.open == True:
				suite.finish()		
		
	def write(self, file):
		self.finish()
		doc = Document()
		root = doc.createElement("testsuites")
		doc.appendChild(root)
		for suite in self.testsuites:
			root.appendChild(suite.toXml(doc))
		file.write(doc.toprettyxml("\t"))	
	
	
class TestSuite():
	def __init__(self, name, hostname):
		self.properties = []
		self.name = name
		self.hostname = hostname
		self.open = False
		self.cases = []
		self.systemout = None
		self.systemerr = None
		
	def start(self):
		self.open = True
		self.time = datetime.now()
		self.timestamp = datetime.isoformat(self.time)
		return self
		
		
	def createCase(self, name, classname=""):
		if self.open:
			case = TestCase(name, classname)
			self.cases.append(case)
			return case
		else:
			raise Exception("This test suite cannot be modified in its current state")
	
	def appendProperty(self, name, value):
		self.properties.append([name, value])
		
	def finish(self, output = None, error = None):
		if self.open == True:
			self.open = False
			# set the number of test cases, error cases, failed cases, and the amount of time taken in seconds.
			td = datetime.now() - self.time
			self.time = float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6
			self.errors = 0
			self.failures = 0
			for case in self.cases:
				if case.state == None:
					case.error("XmlUnit Finished", "The test was forced to finish since the suite was finished.")
				status = case.state.lower()
				if status == "failure":
					self.failures += 1
				elif status == "error":
					self.errors += 1
				else:
					print status
			self.tests = len(self.cases)
			self.output = output
			self.error = error
			return None
		else:
			raise Exception("This test suite is already finished.")
	
	def toXml(self, doc):
		node = doc.createElement("testsuite")
		node.setAttribute("name", self.name)
		node.setAttribute("hostname", self.hostname)
		node.setAttribute("timestamp", self.timestamp)
		node.setAttribute("tests", "%s" % self.tests)
		node.setAttribute("failures", "%s" % self.failures)
		node.setAttribute("errors", "%s" % self.errors)
		node.setAttribute("time", "%s" % self.time)
		for case in self.cases:
			node.appendChild(case.toXml(doc))
		
		return node
	
class TestCase():
	
	def __init__(self, name, classname):
		self.state = None
		self.name = name
		self.classname = classname
		return None
	
	def start(self):
		self.time = datetime.now()
		return self
	
	def custom(self, state, type, message):
		if self.state != None:
			raise Exception("This test case is already finished.")
		self.state = state
		self.message = message
		self.type = type
		td = datetime.now() - self.time
		self.time = float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6
	
	def fail(self, type, message):
		self.custom("failure", type, message)
	
	def skip(self, type, message):
		self.custom("skipped", type, message)
		
	def error(self, type, message):
		self.custom("error", type, message)
			
	def succeed(self):
		if self.state != None:
			raise Exception("This test case is already finished.")
		self.state = "success"
		td = datetime.now() - self.time
		self.time = float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6
		
	def toXml(self, doc):
		node = doc.createElement("testcase")
		node.setAttribute("name", self.name)
		node.setAttribute("classname", self.classname)
		node.setAttribute("time", "%s" % self.time)
		if self.state != "success":
			subnode = doc.createElement(self.state)
			subnode.setAttribute("type", self.type)
			subnode.setAttribute("message", self.message)
			node.appendChild(subnode)
		return node