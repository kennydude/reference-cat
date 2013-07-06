# Web Backend
import web, sys

urls = (
	'/(.*)', 'hello'
)
app = web.application(urls, globals())

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

class hello:
	@endpoint
	def GET(self, name):
		if not name: 
			name = 'World'
		return 'Hello, ' + name + '!'

def launch():
	sys.argv = []

	print(">> Web GUI starting...")
	print(">> Please open a web browser at http://localhost:8080")

	# TODO
	print(">> Note: External connections are disabled")
	app.run()