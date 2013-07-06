from setuptools import setup, find_packages

setup(
	name='ReferenceCat',
	version='0.2dev',
	packages=['referencecat','referencecat.gui.gtk','referencecat.core'],
	include_package_data = True,
	license='Creative Commons Attribution-Noncommercial-Share Alike license',
	long_description=open('README.md').read(),
	url="https://github.com/kennydude/reference-cat",
	author="Joe Simpson",
	author_email="headbangerkenny@gmail.com",
	install_requires=["pystache","web.py"]
)