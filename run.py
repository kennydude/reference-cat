#!/usr/bin/python3
print("ReferenceCat by @kennydude")
print("Version 0.1")

import importlib

gui_libs = ["gtk", "web"]

'''
TODO: Implement and test
if commandLine --gui=x:
	gui_libs = [ x ] + gui_libs
'''

gui = False
for lib in gui_libs:
	try:
		print("> Try to load %s GUI Library" % lib)
		gui = importlib.import_module("gui.%s" % lib)
		print("> %s GUI library loaded" % lib)
		break
	except Exception as e:
		print(">> Could not load %s" % lib)
		print(">> Reason: %s" % e)

if gui != False:
	print("> GUI Starting...")
	gui.launch()
else:
	print("> No GUI could be loaded. ReferenceCat is leaving")