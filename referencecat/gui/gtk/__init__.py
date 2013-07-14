# GTK for ReferenceCat
# I know it's a long file, but it's GTK in one place
# the only other file is a glade file
# If someone wanted to tidy this up, then please do

from gi.repository import Gtk, GObject, Gdk, Pango
from core.reference import *
from core.document import *
import datetime, json, os.path

# TODO: Remove
VERSION = "0.2"

class GReference(GObject.GObject):
	def __init__(self, reference):
		GObject.GObject.__init__(self)
		self.reference = reference
	def __str__(self):
		label = "Unknown Type"
		for (key, s) in SourceTypeStrings:
			if self.reference.type == key:
				label = s
		return "<b>%s:</b> %s" % (label, self.reference.to_html())

class MyApplication(object):
	def open(self):
		print(">> Opening GTK UI")
		self.editIter = None # By default, we append
		self.dirty = False # By default, we are not dirty
		self.filename = None
		self.full_filename = None

		self.builder = Gtk.Builder()
		self.builder.add_from_file("referencecat/gui/gtk/ui.glade")
		self.setupEditReference()

		self.win = self.builder.get_object("mainWindow")
		self.win.connect("delete-event", self.onExit)
		self.win.connect("check-resize", self.winResize)

		self.cell = Gtk.CellRendererText(markup=0)
		self.cell.set_property("wrap_mode", Pango.WrapMode.WORD)
		self.cell.set_property("wrap_width", 500)
		self.cell.set_property("width", 500)
		
		column = Gtk.TreeViewColumn("Reference", self.cell)
		column.set_cell_data_func(self.cell, self.get_name)

		self.store = Gtk.ListStore(GReference.__gtype__)
		
		view = self.builder.get_object("mainList")
		view.set_model(self.store)
		view.connect("row-activated", self.openReferenceForEditing)
		view.append_column(column)

		# Toolbar
		## New item
		add_button = self.builder.get_object("newItem")
		add_button.connect("clicked", self.addNewItem)
		## Save current
		save_button = self.builder.get_object("save")
		save_button.connect("clicked", self.saveCurrent)
		## Open Existing file
		open_button = self.builder.get_object("open")
		open_button.connect("clicked", self.openFileButton)
		## Create new file
		new_button = self.builder.get_object("new")
		new_button.connect("clicked", self.newFile)
		## Export
		export_buttton = self.builder.get_object("export")
		export_buttton.connect("clicked", self.exportReferences)

		self.win.show_all()
		Gtk.main()

	def winResize(self, n=None):
		w = 8
		self.cell.set_property("wrap_width", self.win.get_allocation().width - w )
		self.cell.set_property("width", self.win.get_allocation().width - w )

	def exportReferences(self, a=None):
		export = self.builder.get_object("exportWindow")
		export.set_transient_for( self.win )
		export.show_all()

	def onExit(self, a=None, x=None):
		if self.promptDirtySave() == False:
			return False
		Gtk.main_quit()

	def promptDirtySave(self):
		if self.dirty:
			dialog = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING,
				Gtk.ButtonsType.NONE, "You might loose changes")
			dialog.format_secondary_text("You have made changes in the current document. Do you want to save them?")
			dialog.add_button("Save", Gtk.ResponseType.YES)
			dialog.add_button("Discard", Gtk.ResponseType.NO)
			dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)

			response = dialog.run()
			if response == Gtk.ResponseType.YES:
				print(">> Saving changes")
				self.saveCurrent()
			elif response == Gtk.ResponseType.CANCEL:
				print(">> Stopp!!!")
				dialog.destroy()
				return False
			else:
				print(">> Use does not care about changes")

			dialog.destroy()
		return True

	def newFile(self,a=None):
		if self.promptDirtySave() == False:
			return

		self.full_filename = None
		self.filename = None
		self.wipeView()
		self.updateTitle()

	def setDirty(self, dirty):
		self.dirty = dirty
		self.updateTitle()

	def setFilename(self, filename):
		self.full_filename = filename
		self.filename = os.path.basename(filename)
		self.updateTitle()

	def updateTitle(self):
		parts = ["ReferenceCat"]
		if self.dirty:
			parts.append("Modified")
		if self.filename != None:
			parts.append(self.filename)
		self.win.set_title(" - ".join(parts))

	def openFileButton(self, a=None):
		dialog = Gtk.FileChooserDialog("Open File", self.win,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.addFilters(dialog)
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			if self.promptDirtySave() == False:
				return # Do not override!

			f = dialog.get_filename()
			print( ">> Opening: %s" % f )
			dialog.destroy()
			if self.openFile(f):
				# New filename
				self.setFilename(f)
				# And of course, we are not dirty!
				self.setDirty(False)
		elif response == Gtk.ResponseType.CANCEL:
			print(">> Open Canceled")
			dialog.destroy()

	def openFile(self,filename):
		try:
			f = open(filename, 'r')

			d = Document()
			d.input( f.read() )

			#data = json.load(f)
			f.close()

			if(d.version != VERSION):
				self.showInfo("File saved with a different version of ReferenceCat!", "The file was opened with a differnet version. Some things may not work correctly, but we will try")
			
			self.wipeView()
			for item in d.references:
				self.addReferenceToList(item)
			return True
		except Exception as e:
			self.showInfo("Could not open file", "An error occured. The error was: %s" % e)
			return False

	def wipeView(self):
		# Remove all items from list
		self.store.clear()

	def saveCurrent(self,a=None):
		if self.full_filename != None:
			self.saveFile( self.full_filename )
			return

		dialog = Gtk.FileChooserDialog("Save file", self.win,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_current_name("references.refcat")
		self.addFilters(dialog)
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			f = dialog.get_filename()
			print( ">> Saving: %s" % f )
			dialog.destroy()
			self.saveFile( f )
		elif response == Gtk.ResponseType.CANCEL:
			print(">> Save Canceled")
			dialog.destroy()

	def saveFile(self, filename):
		try:
			f = open(filename, 'w')
			arr = []
			for x in range(0, self.store.iter_n_children(None)):
				arr.append( self.store.get(self.store.iter_nth_child(None,x), 0)[0].reference )
			# json.dump(, f)

			d = Document()
			d.references = arr
			f.write( d.output() )

			f.close()

			# We are no longer dirty!
			self.setDirty(False)
			# Set the first bit of a filename
			self.setFilename(filename)
		except Exception as e:
			self.showInfo("Could not save file", "An error occured. The error was: %s" % e)

	def showInfo(self, title, text):
		dialog = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.INFO,
									Gtk.ButtonsType.OK, title)
		dialog.format_secondary_text(text)
		dialog.run()
		dialog.destroy()

	def addFilters(self, dialog):
		filter_py = Gtk.FileFilter()
		filter_py.set_name("ReferenceCat")
		filter_py.add_mime_type("text/x-reference-cat")
		filter_py.add_pattern("*.refcat")
		dialog.add_filter(filter_py)

	def openReferenceForEditing(self, tree, a, b):
		# Open the selected reference for editing
		it = self.store.get_iter(a)
		self.editIter = it # This variable is set so we do not append
		ref = self.store[it][0].reference
		# Set the instance to edit
		self.ref = ref

		# Get ready to show the reference
		add = self.builder.get_object("editReference")
		add.set_title("Edit reference")
		add.set_transient_for( self.win )
		add.show_all()

		self.stripGrid( self.builder.get_object("grid") )

		typeBox = self.builder.get_object("cbType")
		i = 0
		for (key,v) in SourceTypeStrings:
			if key == ref.type:
				j = i
			i+=1
		typeBox.set_active(j)
		self.editReferenceTypeChange(typeBox)

		# You can't delete non-existant references
		deleteButton = self.builder.get_object("tbDelete")
		deleteButton.show()

	def addReferenceToList(self, reference):
		# This needs wrapping because GObject stuff complains about
		# "reference not being a GObject" and I don't want to break
		# that class's generic-ness
		self.store.append([GReference( reference )] )

	def addNewItem(self, x):
		# Called when the new reference
		# button is pressed.
		# We set things up for new items
		self.ref = Reference()
		self.editIter = None

		add = self.builder.get_object("editReference")
		add.set_title("Add new Reference")
		add.set_transient_for( self.win )
		add.show_all()

		self.stripGrid( self.builder.get_object("grid") )

		typeBox = self.builder.get_object("cbType")
		typeBox.set_active(-1)

		# You can't delete non-existant references
		deleteButton = self.builder.get_object("tbDelete")
		deleteButton.hide()

	def setupEditReference(self):
		# This method is needed because of single
		# instances and we only need to do this once

		add = self.builder.get_object("editReference")
		add.connect("delete-event", self.editReferenceDelete)

		typeStore = Gtk.ListStore(str,str)
		for (key, value) in SourceTypeStrings:
			typeStore.append( [key,value] )
		# TODO: Move exact def somewhere else
		#typeStore.append([ "book", "Whole Book" ])
		#typeStore.append([ "chapter", "Book Chapter" ])
		#typeStore.append([ "journal", "Journal Article" ])
		#typeStore.append([ "web", "Website" ])
		typeBox = self.builder.get_object("cbType")
		typeBox.set_model(typeStore)
		typeBox.set_property("name", "typeBox")

		renderer_text = Gtk.CellRendererText()
		typeBox.pack_start(renderer_text, True)
		typeBox.add_attribute(renderer_text, "text", 1)
		typeBox.connect("changed", self.editReferenceTypeChange)

		lblType = self.builder.get_object("lblType")
		lblType.set_property("name", "lblType")

		addButton = self.builder.get_object("tbAddRef")
		addButton.set_sensitive(False)
		addButton.connect("clicked", self.saveReferenceButtonPress, add)

		gettingStarted = self.builder.get_object("lblGetStarted")
		gettingStarted.set_property("name", "gettingStarted")

	def editReferenceDelete(self, win, x):
		win.hide()
		return True

	def saveReferenceButtonPress(self, button, win):
		self.setDirty(True)
		if self.editIter == None:
			self.addReferenceToList( self.saveReference() )
		else:
			# Replace
			self.store.set_value( self.editIter, 0, GReference( self.saveReference() ) )
		win.hide()

	def saveReference(self):
		# Save reference that is being edited in the dialog right now

		print("> Save Reference")
		reference = Reference()

		# Get active type
		add = self.builder.get_object("editReference")
		combo = self.builder.get_object("cbType")
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		intName, name = model[tree_iter][:2]
		reference.type = intName

		fields = getFieldsBySourceType( intName )

		grid = self.builder.get_object("grid")
		# Now we loop through the GUI elements
		# getting their data and setting it to the reference
		# instance we made earlier
		for child in grid.get_children():
			name = child.get_data("property")
			if name != None:
				data = {}
				for x in fields:
					if x['key'] == name:
						data = x

				if data['type'] == "PeopleList":
					people = []
					for person in child.get_children():
						if person.get_data("role") == "author":
							if person.get_text().strip() != "": # Blank people are not people 
								people.append(person.get_text())
					setattr(reference, data['key'], people)
				elif data['type'] == "Date":
					day = 0
					month = 0
					year = 0
					# loop through and set the children
					for x in child.get_children():
						name = x.get_property("name")
						if name == "day":
							day = int(x.get_value())
						elif name == "month":
							tree_iter = x.get_active_iter()
							model = x.get_model()
							number, name = model[tree_iter][:2]
							month = number - 1
						elif name == "year":
							year = int(x.get_value())
						# Sorry Americans, we store dates in a BRITTISH!!!! fashion
						# (don't worry, you won't really see it, we can mix the UI up for you)
						setattr(reference, data['key'], "%s/%s/%s" % (day,month,year))
				elif data['type'] == "Year":
					setattr(reference, data['key'], int(child.get_value()))
				else:
					setattr(reference, data['key'], child.get_text())
		return reference

	def stripGrid(self, grid, hideGS=False):
		# Strip the grid
		children = grid.get_children()
		for child in children:
			name = child.get_property("name")
			if name == "gettingStarted":
				if hideGS:
					child.hide()
				else:
					child.show()
			elif name != "lblType" and name != "typeBox":
				child.destroy()

	def editReferenceTypeChange(self, combo):
		tree_iter = combo.get_active_iter()
		model = combo.get_model()
		intName, name = model[tree_iter][:2]
		print(">> Reference Type %s selected" % intName)
		fields = getFieldsBySourceType( intName )

		grid = self.builder.get_object("grid")

		# Enable dismiss button now we have set a type
		addButton = self.builder.get_object("tbAddRef")
		addButton.set_sensitive(True)

		self.stripGrid(grid, True)

		# Now re-create it
		top = 1
		for data in fields:
			label = Gtk.Label()
			label.set_text( "%s:" % data['title'] )
			label.set_property("margin-right", 8)
			label.set_property("halign", Gtk.Align.END)
			label.show()
			grid.attach(label, 0, top, 1, 1)

			# Now the editor
			if data['type'] == "PeopleList":
				ed = Gtk.Grid()
				ed.set_data("rowAt", 0)

				for author in getattr(self.ref, data['key']):
					self.addPeopleListRow(None, ed, -1, author)

				self.addPeopleListRow(None, ed, -1)
				
				new_row = Gtk.Button("Add")
				new_row.connect("clicked", self.addPeopleListRow, ed)
				ed.attach(new_row, 0, ed.get_data("rowAt")+1, 2, 1)

			elif data['type'] == "Year":
				ed = Gtk.SpinButton()
				value = getattr(self.ref, data['key'])
				# I hope nobody is using this in the year 4,000!
				ed.set_adjustment( Gtk.Adjustment(value, 0, 4000, 1, 10, 0) )
				ed.set_numeric(True)
			elif data['type'] == "Date":
				ed = Gtk.Box(spacing=4)

				value = getattr(self.ref, data['key'])
				if value != "":
					value = value.split("/")
					print(">> %s" % value)
					date = datetime.date( int(value[2]), int(value[1]), int(value[0]) )
				else:
					date = datetime.date.today()

				# Create the date picker
				today = Gtk.Button("Set to Today")
				today.connect("clicked", self.setToToday, ed)
				ed.pack_start(today, True, True, 0)

				day = Gtk.SpinButton()
				day.set_property("name", "day")
				value = date.day
				day.set_numeric(True)
				day.set_adjustment( Gtk.Adjustment(value, 1, 31, 1, 10, 0) )
				ed.pack_start(day, True, True, 0)

				month = self.get_month_picker(date.month)
				month.set_property("name", "month")
				ed.pack_start(month, True, True, 0)

				year = Gtk.SpinButton()
				year.set_property("name", "year")
				value = date.year
				year.set_adjustment( Gtk.Adjustment(value, 0, 4000, 1, 10, 0) )
				year.set_numeric(True)
				ed.pack_start(year, True, True, 0)
			else:
				ed = Gtk.Entry()
				ed.set_text( getattr(self.ref, data['key']) )

			ed.set_property("name", "editProp%s" % data['key'])
			ed.set_property("hexpand", True)
			ed.set_data("property", data['key'])
			ed.show_all()
			grid.attach(ed, 1, top, 1,1)

			top += 1

	def addPeopleListRow(self, ed, grid, row = -1, text=None):
		print(">> Add people list row")
		# We need to find out our next row and work with it

		if row == -1:
			row = grid.get_data("rowAt")
			row += 1
			grid.set_data("rowAt", row)
			grid.insert_row(row)
			print(">> Insert row %s" % row)

		e = Gtk.Entry()
		e.set_property("placeholder-text", "e.g: John Smith")
		e.set_property("name", "editAuthor%s" % row)
		e.set_data("role", "author")
		if text != None:
			e.set_text(text)
		grid.attach(e, 0, row, 1, 1)

		remove = Gtk.Button("-")
		# TODO: Use an icon instead
		remove.set_property("name", "remove%s" % row)
		remove.connect("clicked", self.removePeopleListRow, grid)
		grid.attach(remove, 1, row, 1, 1)

		grid.show_all()

	def removePeopleListRow(self, removeButton, grid):
		row = int( removeButton.get_property("name")[6:] )
		# Remove the Remove button
		grid.remove(removeButton)
		removeButton.destroy()
		for child in grid.get_children():
			if child.get_property("name") == "editAuthor%s" % row:
				# Remove the Author edit text
				grid.remove(child)
				child.destroy()

	def setToToday(self, todayButton, box):
		today = datetime.date.today()
		for child in box.get_children():
			name = child.get_property("name")
			if name == "day":
				child.set_value( today.day )
			elif name == "month":
				child.set_active( today.month - 1 )
			elif name == "year":
				child.set_value( today.year )

	def get_month_picker(self, month=6):
		monthStore = Gtk.ListStore(int,str)
		monthStore.append([1, "January"])
		monthStore.append([2, "February"])
		monthStore.append([3, "March"])
		monthStore.append([4, "April"])
		monthStore.append([5, "May"])
		monthStore.append([6, "June"])
		monthStore.append([7, "July"])
		monthStore.append([8, "August"])
		monthStore.append([9, "September"])
		monthStore.append([10, "October"])
		monthStore.append([11, "November"])
		monthStore.append([12, "December"])
		monthBox = Gtk.ComboBox()

		monthBox.set_model(monthStore)
		renderer_text = Gtk.CellRendererText()
		monthBox.pack_start(renderer_text, True)
		monthBox.add_attribute(renderer_text, "text", 1)

		monthBox.set_active(month-1)
		#monthBox.set ( monthStore.iter_nth_child(None, 0)  )

		return monthBox

	def get_name(self,column, cell, model, iter, data):
		cell.set_property('markup', str(self.store.get_value(iter, 0)))

def launch():
	try:
		import signal
		signal.signal(signal.SIGINT, signal.SIG_DFL)
	except Exception as ex:
		print(">> ReferenceCat could not correctly set the Ctrl+C behaviour. Sorry :(")
		print(">>> What happened was: %s" % ex)
		prinT(">>> However, don't worry as this is not critical.")
	MyApplication().open()