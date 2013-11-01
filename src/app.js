// ReferenceCat Version 2
// This code isn't how I wanted it, but heck it works <3
// Sorry, but this is Node-Webkit only for now!

var fs = require("fs");

var current_version = 2;

function setupItem(item){
	// Setup the type field on the editor template
	var typeS = $(".type", item).each(function(){
		var types = Object.keys(ReferenceData.types);
		for(type in types){
			type = types[type];
			$("<option />").attr("value", type).html(t("types." + type)).appendTo(this);
		}
	}).on('change', function(){
		var master = $(this).closest('.item'),
			bottom = $(".bForm", master);
		$(".editor_group", master).remove();

		if(ReferenceData.types[$(this).val()] == undefined){
			console.log("Non-proper item: " + $(this).val());
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

			var ed = $("<div/>").addClass('editor_group control-group').insertBefore(bottom);
			$("<label/>").text(t("fields." + fieldname)).appendTo(ed);

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
					var div = $("<div />").appendTo(ed),
						addRowD = $("<div />").html("Add new row").appendTo(div).addClass("inline"),
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

	if($(item).data("type")){
		typeS.val($(item).data("type")).change();
	}

	$(".editorSwitch", item).click(function(){
		$(".editor", $(this).closest(".item").toggleClass("editing")).toggleClass("hide");
	});

	$(".deleteItem", item).click(function(){
		if(confirm(t("messages.delete_item"))){
			$(this).closest("li").remove();
		}
	});
}

/**
 * Renders a reference
 * @param item <div class=.item>
 */
function render_reference(item){
	// Build input
	try{
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
		$(".reference", item).html( ReferenceData.types[$(item).data('type')].list_template(context) );
	} catch(e){}
}

function buildItem(){
	var ix = $(".itemtemplate").clone().removeClass("hide itemtemplate"),
		li = $("<li/>");
	ix.appendTo(li);
	return li.appendTo(".contents");
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
	var item = buildItem();
	setupItem(item);
});

var currentFilePath = undefined;

function reallySaveFile(data){
	$("#saveFile").html('<i class="glyphicons stopwatch"></i>');
	$.get("src/file.html", function(templateData){
		var template = Handlebars.compile(templateData);
		var dataToSave = template({
			"data" : JSON.stringify(data),
			"reference" : [] // TODO
		});
		console.log(currentFilePath);
		fs.writeFile(currentFilePath, dataToSave, function(err){
			if(!err){
				$("#saveFile").removeClass("unsaved").html('<i class="glyphicons disk_save"></i>');
				$(".versionMismatch, .saveFailure").addClass("hide"); // No longer mismatched
			} else{
				$("#saveFile").html('<i class="glyphicons stopwatch"></i>');
				$(".saveFailure").removeClass('hide');
			}
		});
	});
}

$("#saveFile").click(function(){
	var data = {"version" : current_version, "data" : [], "format" : "harvard"};
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
		$("<input type=file nwsaveas='references.refcat' accept='.refcat' />").change(function(){
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
		if(!confirm(t("messages.loose_changes"))){
			return false;
		}
	}
	// We need to clear the UI now
	$("#saveFile").removeClass("unsaved");
	$(".contents").html('');
	$(".versionMismatch").addClass("hide");

	cb();
}

$("#newFile").click(function(){
	newFile(function(){});
});

$("#openFile").click(function(){
	$("<input type=file accept='.refcat' />").change(function(){
		var fname = $(this).val();
		newFile(function(){
			fs.readFile(fname, function(err, data){
				if(err){
					alert(t("errors.load"));
				} else{
					// Find JSON data
					data = data.toString();

					var tag = '<script type="text/json">',
						i = data.indexOf(tag) + tag.length,
						e = data.indexOf('</script>', i);
					data = data.substring(i, e).trim();
					data = JSON.parse(data);


					// Now we have JSON, check the version
					if(data.version != current_version){
						$(".versionMismatch").removeClass("hide");
					}

					// Load in all of the references
					data.data.forEach(function(ref){
						var item = buildItem();
						for(key in ref){
							item.data(key, ref[key]);
						}
						setupItem(item);
						render_reference(item);
					});

					// Finally set the current file path
					currentFilePath = fname;
				}
			});
		});
	}).click();
});

// Translation stuff
$(".translateTitle").each(function(){
	$(this).attr("title", t($(this).data("title")));
});
$(".translateContent").each(function(){
	$(this).html( t($(this).html()) );
});

// App UI
$(window).on('resize', function(){
	$(".contents").css("height", ($(window).height() - $(".chrome").height()) + "px");
}).trigger('resize');

setTimeout(function(){
	$(window).trigger('resize');
}, 2000);