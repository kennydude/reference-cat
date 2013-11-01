// ReferenceCat Version 2
// This code isn't how I wanted it, but heck it works <3
// Sorry, but this is Node-Webkit only for now!

var fs = require("fs");

function setupItem(item){
	// Setup the type field on the editor template
	$(".type", item).each(function(){
		var types = Object.keys(ReferenceData.types);
		for(type in types){
			type = types[type];
			$("<option />").attr("val", type).html(type).appendTo(this);
		}
	}).on('change', function(){
		var master = $(this).closest('.item'),
			bottom = $(".bForm", master);
		$(".editor_group", master).remove();

		if(ReferenceData.types[$(this).val()] == undefined){
			console.log("Non-proper item");
			master.removeClass("proper");
			return;
		}

		master.data("type", $(this).val()).addClass("proper");

		var data = ReferenceData.types[$(this).val()].fields;
		data.forEach(function(fieldname){
			var fdata = ReferenceData.fields[fieldname],
				update_val = function(val){
					console.log(fieldname, val);
					master.data(fieldname, val);
					$("#saveFile").addClass("unsaved");
					render_reference(master);
				};

			var ed = $("<div/>").addClass('editor_group pure-control-group').insertBefore(bottom);
			$("<label/>").text(fieldname).appendTo(ed);

			switch(fdata['type']){
				// Basically we switch based on data-type
				// Then you build your element.
				// Values can be got: master.data(fieldname)
				// Set values: update_val(newval);
				case "string":
					$("<input>").attr("type", "text").val(master.data(fieldname)).appendTo(ed).change(function(){
						update_val($(this).val());
					});
					break;
				case "year":
					var v = master.data(fieldname);
					if(!v){ v = new Date().getFullYear(); }
					$("<input>").attr("type", "number").val(v).appendTo(ed).change(function(){
						update_val($(this).val());
					});
					update_val(v);
					break;
				case "url":
					$("<input>").attr("type", "url")
						.attr("placeholder", "(copy and pasting is easiest)")
						.val(master.data(fieldname))
						.appendTo(ed)
						.change(function(){
							update_val($(this).val());
						});
					break;
				case "date":
					var v = master.data(fieldname);
					if(!v){ v = moment().format("YYYY-MM-DD"); }
					$("<input>").attr("type", "date").val(v).appendTo(ed).change(function(){
						update_val($(this).val());
					});
					update_val(v);
					break;
				case "string[]":
					var div = $("<div />").appendTo(ed).addClass("pure-form-message-inline"),
						addRowD = $("<div />").html("Add new row").appendTo(div),
						addRow = function(){
							$("<input>").attr("type", "text")
								.change(function(){

								})
								.attr("placeholder", fdata['placeholder'])
								.insertBefore(addRowD);
						};
					addRow();
					addRowD.click(addRow);
					break;
			}
		});
	});

	$(".editorSwitch", item).click(function(){
		$(".editor", $(this).closest(".item").toggleClass("editing")).toggleClass("hide");
	});
}

/**
 * Renders a reference
 * @param item <div class=.item>
 */
function render_reference(item){
	// Build input
	var data = ReferenceData.types[$(item).data('type')].fields,
		context = {};
	data.forEach(function(fieldname){
		var fdata = ReferenceData.fields[fieldname];
		switch(fdata['type']){
			case "date":
			case "year":
			case "url":
			case "string":
			case "string[]":
				context[fieldname] = $(item).data(fieldname);
				break;
		}
	});

	// Just render it :P
	$(".reference", item).html( markdown.toHTML(ReferenceData.types[$(item).data('type')].list_template(context)) );
}

Handlebars.registerHelper('date_render', function(d, format) {
	return moment(d).format(format);
});

// Compile me templates
for(name in ReferenceData.types){
	var type = ReferenceData.types[name];
	if(type.list_template)
		type.list_template = Handlebars.compile(type.list_template);
};


$(".newitem").click(function(){
	var item = $(".itemtemplate").clone().removeClass("hide itemtemplate").appendTo(".contents");
	setupItem(item);
});

var currentFilePath = undefined;

function reallySaveFile(data){
	$("#saveFile").html("Saving....");
	$.get("src/file.html", function(templateData){
		var template = Handlebars.compile(templateData);
		var dataToSave = template({
			"data" : JSON.stringify(data),
			"reference" : [] // TODO
		});
		console.log(currentFilePath);
		fs.writeFile(currentFilePath, dataToSave, function(err){
			if(!err){
				$("#saveFile").removeClass("unsaved").html("Save");
			} else{
				$("#saveFile").html("Save (!)");
			}
		});
	});
}

$("#saveFile").click(function(){
	var data = {"version" : 2, "data" : [], "format" : "harvard"};
	$(".contents .item.proper").each(function(){
		var elem = {"type" : $(this).data("type")};

		var fields = ReferenceData.types[$(this).data('type')].fields,
			self = this;
		fields.forEach(function(fieldname){
			var fdata = ReferenceData.fields[fieldname];
			elem[fieldname] = $(self).data(fieldname);
		});

		data.data.push(elem);
	});

	if(currentFilePath == undefined){
		$("<input type=file nwsaveas='references.referencecat' accept='.referencecat' />").change(function(){
			currentFilePath = $(this).val();
			reallySaveFile(data);
		}).click();
	} else{
		reallySaveFile(data);
	}
});

function newFile(cb){
	if($("#saveFile").hasClass("unsaved")){
		// Unsaved changes :O
		// I really wish there was a better way
		if(!confirm("If you continue, your changes will be lost")){
			return false;
		}
	}
	// We need to clear the UI now
	$("#saveFile").removeClass("unsaved");
	$(".contents").html('');

	cb();
}

$("#openFile").click(function(){
	$("<input type=file accept='.referencecat' />").change(function(){
		newFile(function(){
			// todo
		});
	}).click();
});