// Harvard Referencing System Data
window.ReferenceData = {
	"types" : {
		"book" : {
			"fields" : [
				"author",
				"year",
				"title",
				"edition",
				"place_publication",
				"page"
			]
		},
		"wiki" : {
			"fields" : [
				"title",
				"year",
				"website_name",
				"url",
				"date_accessed"
			],
			"list_template" : "'{{title}}' ({{year}}) <i>{{website_name}}</i>. Available at: {{url}} (Accessed: {{date_render date_accessed 'DD MMMM YYYY'}})"
		},
		"web" : {
			"fields" : [
				"title",
				"url",
				"date_accessed"
			]
		}
	},
	"fields" : {
		"title" : {
			"type" : "string"
		},
		"year" : {
			"type" : "year"
		},
		"author" : {
			"type" : "string[]",
			"placeholder" : "e.g John Howard Smith"
		},
		"publisher" : {
			"type" : "string"
		},
		"website_name" : {
			"type" : "string"
		},
		"url" : {
			"type" : "url"
		},
		"date_accessed" : {
			"type" : "date"
		}
	}
};