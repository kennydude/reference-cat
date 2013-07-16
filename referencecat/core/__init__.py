VERSION = "0.1"

from core import reference
from core import document
import sys,traceback

def print_exception():
	exc_type, exc_value, exc_traceback = sys.exc_info()
	print "*** print_exception:"
	traceback.print_exception(exc_type, exc_value, exc_traceback,
	                          limit=9, file=sys.stdout)