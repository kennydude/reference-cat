module.exports = function(grunt) {

	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json')
	});

	grunt.registerTask('reference', 'Compile the reference files', function(){
		// Okay, I have no idea if this is correct
		var fs = require('fs');
		var styles = fs.readdirSync('referencing');
		styles.forEach(function(style){
			if(style.indexOf(".") === 0) return; // Damn .DS_Store, I hate you!

			grunt.log.writeln('Generating data/' + style + '.js');

			var data = {"types" : {}};

			var objects = fs.readdirSync('referencing/' + style);
			objects.forEach(function(object){
				if(object.indexOf('.ref') !== object.length-4) return;
				object = object.substring(0, object.length-4);

				grunt.log.writeln('> Adding object ' + object);
				var ofile = fs.readFileSync('referencing/' + style + '/' + object + '.ref').toString(),
					parts = ofile.split('\n---\n');

				if(!parts[3]) parts[3] = '';

				data.types[object] = {
					"fields" : parts[0].split(" "),
					"description" : parts[1],
					"list_template" : parts[2],
					"in_text_template" : parts[3]
				};
			});

			// TODO: Write to a real file
			console.log(JSON.stringify(data, null, '\t'));
		});
	});


	// Default task(s).
	grunt.registerTask('default', ['reference']);

};