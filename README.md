# ReferenceCat

todo

# Referencing Files

Files in referencing build up the data javascript files the application uses.

The format is very basic of these files. You simply place in the directory of your style's name a file named
"<type-of-object-being-referenced>.ref"

The file is split up by markers: ---

4 sections are in the file:

* List of fields (space separated) the object needs
* Description. Markdown allowed
* Reference List rendering (Handlebars)
* In-text citation (optional, again Handlebars)

All translations are done elsewhere!