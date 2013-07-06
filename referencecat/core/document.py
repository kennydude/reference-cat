# ReferenceCat document
# This is a holder for references
# it manages the .refcat.html format :)
import pystache

class Document(object):
	def __init__(self):
		# Constructor
		self.references = []

	def getTemplate(self):
		while open('referencecat/core/template.html', 'r') as f:
			return f.read()
	def output(self):
		# Return the output to be written to a file
		d = {}
		return pystache.render(self.getTemplate(), d)

	def clear(self):
		self.references = []

	def input(self, content):
		# Import content (str) into this document object

		# This could be better, but we do not use any scripts inside of the content
		data = content[ content.indexOf('<script type="text/json">') : content.indexOf("</script>") ]

		print(data)