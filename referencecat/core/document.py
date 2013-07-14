# ReferenceCat document
# This is a holder for references
# it manages the .refcat.html format :)
import pystache, json, string
from core.reference import Reference

# TODO: Move
VERSION = "0.2"

class Document(object):
	def __init__(self):
		# Constructor
		self.version = VERSION
		self.references = []

	def getTemplate(self):
		with open('referencecat/core/template.html', 'r') as f:
			return f.read()
	def getReferenceKey(self, r):
		o = r.author_string(r.author) + str(r.year)
		print o
		return o
	def output(self):
		# Return the output to be written to a file
		d = {}

		# Sort them alphabetically by Author
		self.references = sorted( self.references, key=self.getReferenceKey )

		x = []
		r = []
		for reference in self.references:
			x.append( reference.to_object() )
			r.append({
				"reference" : reference.to_html()
			})

		d['raw_data'] = json.dumps({
			"version" : VERSION,
			"data" : x
		})
		d['references'] = r
		d['version'] = VERSION
		return pystache.render(self.getTemplate(), d)

	def clear(self):
		self.references = []

	def input(self, data):
		# Import content (str) into this document object

		# This could be better, but we do not use any scripts inside of the content
		if '<script type="text/json">' in data:
			data = data[ data.find('<script type="text/json">') : data.find("</script>") ]
		data = data[ data.find('{') : data.rfind('}')+1 ]

		# Data
		data = json.loads(data)

		# Now we run through it
		self.version = data['version']
		self.references = []
		for item in data['data']:
			reference = Reference()
			reference.from_object(item)
			self.references.append(reference)

