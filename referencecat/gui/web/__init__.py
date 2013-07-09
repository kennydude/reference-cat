# Web Backend
import web, sys, pystache, core

urls = (
	'/', 'main',
	'/jquery.min.js', 'jquery',
	'/moment.min.js', 'moment'
)
app = web.application(urls, globals())
templates = {}
debug = True

def endpoint(cb):
	# this is a decorator which we use to keep security
	# (we don't want security issues)
	def f(*args):
		# when we add settings, this will need a bit more work
		if web.ctx.env['REMOTE_ADDR'] != "127.0.0.1":
			return "401 Unauthorized: This instance of ReferenceCat does not allow external access"
		print(args)
		return cb(*args)
	return f

def template(x, cntx, master=False):
	# x = template name
	# cntx = stuff you want to pass
	# master = do not touch!!!!
	if x in templates:
		renderer = pystache.Renderer()
		o = renderer.render( templates[x], cntx )
		if master:
			return o
		else:
			cntx['content'] = o
			return template("layout", cntx, True)
	else:
		templates[ x ] = pystache.parse( unicode(open('referencecat/gui/web/%s.html' % x).read() ))
		o = template( x, cntx, master )
		if debug:
			del templates[x]
		return o

class jquery:
	@endpoint
	def GET(self):
		return open('referencecat/gui/web/jquery.min.js').read()

class moment:
	@endpoint
	def GET(self):
		return open('referencecat/gui/web/moment.min.js').read()

class main:
	@endpoint
	def GET(self):
		d = {}
		for (key,value) in core.reference.SourceTypeStrings:
			d[key] = {
				"label" : value,
				"fields" : core.reference.getFieldsBySourceType(key)
			};
		return template("start",{"fields":d})

def launch():
	sys.argv = []

	print(">> Web GUI starting...")
	print(">> Please open a web browser at http://localhost:8080")

	# TODO
	print(">> Note: External connections are disabled")
	app.run()