# Reference Class

'''
* type - book/chapter/journal/website
* author(s)
* editor
* chapter title
* page number
* jorunal number
* year
* title
* place of publication
* publisher
* date accessed
* url
'''
import datetime, cgi

# TODO: Make sure it works with python3.4
def enum(**enums):
    return type('Enum', (), enums)

SOURCE_TYPE = enum(
	BOOK = "book",
	BOOK_CHAPTER = "chapter",
	JORUNAL = "journal",
	WEBSITE = "web",
	EMAIL = "email"
)

SourceTypeStrings = [
	("book", "Whole Book"),
	("chapter", "Book Chapter"),
	("journal", "Journal Article"),
	("web", "Website"),
	("email", "Email")
]

def getFieldsBySourceType(sourceType):
	'''
	Get fields required for the source type provided
	It will return a key for them
	and a value containing title and type

	Type can be Text, PeopleList, Year, Date.

	You should use this to populate UI
	'''
	if sourceType == SOURCE_TYPE.EMAIL:
		return [
			{
				"key" : "author",
				"title" : "Author",
				"type" : "PeopleList"
			},
			{
				"key" : "year",
				"title" : "Year",
				"type" : "Year"
			},
			{
				"key" : "date_accessed",
				"title" : "Received Date",
				"type" : "Date"
			},
			{
				"key" : "title",
				"title" : "Email address",
				"type" : "Text"
			}
		]
	elif sourceType == SOURCE_TYPE.BOOK:
		return [
			{
				"key" : "author",
				"title" : "Author",
				"type" : "PeopleList"
			},
			{
				"key" : "year",
				"title" : "Year",
				"type" : "Year"
			},
			{
				"key" : "title",
				"title" : "Title",
				"type" : "Text"
			},
			{
				"key" : "publication_place",
				"title" : "Publication Place",
				"type" : "Text"
			},
			{
				"key" : "publisher",
				"title" : "Publisher",
				"type" : "Text"
			}
		]
	elif sourceType == SOURCE_TYPE.JORUNAL:
		return [
			{
				"key" : "author",
				"title" : "Author",
				"type" : "PeopleList"
			},
			{
				"key" : "year",
				"title" : "Year",
				"type" : "Year"
			},
			{
				"key" : "chapter_title",
				"title" : "Article Title",
				"type" : "Text"
			},
			{
				"key" : "title",
				"title" : "Journal Title",
				"type" : "Text"
			},
			{
				"key" : "volume_number",
				"title" : "Volume Number",
				"type" : "Text"
			},
			{
				"key" : "issue_number",
				"title" : "Issue Number",
				"type" : "Text"
			},
			{
				"key" : "page_number",
				"title" : "Page Numbers",
				"type" : "Text"
			}
		]
	elif sourceType == SOURCE_TYPE.WEBSITE:
		return [
			{
				"key" : "author",
				"title" : "Author",
				"type" : "PeopleList"
			},
			{
				"key" : "year",
				"title" : "Year",
				"type" : "Year"
			},
			{
				"key" : "title",
				"title" : "Website Title",
				"type" : "Text"
			},
			{
				"key" : "url",
				"title" : "URL",
				"type" : "Text"
			},
			{
				"key" : "date_accessed",
				"title" : "Date Accessed",
				"type" : "Date"
			},
		]
	elif SOURCE_TYPE.BOOK_CHAPTER:
		return [
			{
				"key" : "author",
				"title" : "Chapter authors",
				"type" : "PeopleList"
			},
			{
				"key" : "year",
				"title" : "Year",
				"type" : "Year"
			},
			{
				"key" : "chapter_title",
				"title" : "Chapter title",
				"type" : "Text"
			},
			{
				"key" : "editor",
				"title" : "Editors",
				"type" : "PeopleList",
				"help" : "The people who edited the whole book"
			},
			{
				"key" : "title",
				"title" : "Book Title",
				"type" : "Text",
				"help" : "The title of the entire book"
			},
			{
				"key" : "publication_place",
				"title" : "Publication Place",
				"type" : "Text"
			},
			{
				"key" : "publisher",
				"title" : "Publisher",
				"type" : "Text"
			},
			{
				"key" : "page_number",
				"title" : "Page Numbers",
				"type" : "Text"
			}
		]
	else: return []

class Reference(object):
	def __init__(self, saved=None):
		self.type = SOURCE_TYPE.BOOK
		self.author = []
		self.editor = []
		self.chapter_title = ""
		self.page_number = ""
		self.volume_number = ""
		self.issue_number = ""
		self.year = datetime.date.today().year
		self.title = ""
		self.publication_place = ""
		self.publisher = ""
		self.date_accessed = ""
		self.url = ""
	def to_object(self):
		# Serialize to object
		return {
			"type" : self.type,
			"author" : self.author,
			"editor" : self.editor,
			"chapter_title" : self.chapter_title,
			"page_number" : self.page_number,
			"volume_number" : self.volume_number,
			"issue_number" : self.issue_number,
			"year" : self.year,
			"title" : self.title,
			"publication_place" : self.publication_place,
			"publisher" : self.publisher,
			"date_accessed" : self.date_accessed,
			"url" : self.url
		}
	def from_object(self, obj):
		self.type = obj['type']
		self.author = obj['author']
		self.editor = obj['editor']
		self.chapter_title = obj['chapter_title']
		self.page_number = obj['page_number']
		self.volume_number = obj['volume_number']
		self.issue_number = obj['issue_number']
		self.year = obj['year']
		self.title = obj['title']
		self.publication_place = obj['publication_place']
		self.publisher = obj['publisher']
		self.date_accessed = obj['date_accessed']
		self.url = obj['url']
	def author_harvard(self, author):
		# Turn an author into the correct Harvard rendering
		parts = author.split(" ")
		surname = parts.pop(-1).strip()

		initials = []
		for part in parts:
			if part[-1] != ".":
				part += "."
			initials.append(part[0] + part[-1])

		if len(initials) == 0:
			return surname

		return "%s, %s" % ( surname, " ".join(initials) )
	def author_string(self, authors):
		o = []
		for author in authors:
			o.append(self.author_harvard(author))

		end = ''
		if len(o) >= 2:
			end = o[-2] + " and " + o[-1]
			if len(o) >= 3:
				end = " " + end
			del o[-2]
			del o[-1]
		return "%s%s" % ( ", ".join(o), end )
	def to_html(self):
		# Note: This is HTML4 because of Pango, but should render okay
		# TODO: Make a lot better for missing bits out!
		if self.type == SOURCE_TYPE.BOOK:
			return "%s (%s) <i>%s</i> %s: %s" % (
				self.author_string(self.author),
				self.year,
				cgi.escape(self.title),
				cgi.escape(self.publication_place),
				self.publisher
			)
		elif self.type == SOURCE_TYPE.JORUNAL:
			volume = self.volume_number
			if self.issue_number != "":
				volume += " (%s)" % self.issue_number
			return "%s (%s) %s <i>%s</i> %s %s" % (
				self.author_string(self.author),
				self.year,
				cgi.escape(self.chapter_title),
				cgi.escape(self.title),
				volume,
				self.page_number
			)
		elif self.type == SOURCE_TYPE.WEBSITE:
			return "%s (%s) <i>%s</i>. Available from: %s [Accessed %s]" % (
				self.author_string(self.author),
				self.year,
				cgi.escape(self.title),
				cgi.escape(self.url),
				self.date_accessed
			)
		elif self.type == SOURCE_TYPE.EMAIL:
			return "%s %s, email %s, &lt;%s&gt;" % (
				self.author_string(self.author),
				self.year,
				self.date_accessed,
				cgi.escape(self.title)
			)
		return "<b>Unknown Reference Type</b>"