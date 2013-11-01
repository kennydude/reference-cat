// Harvard Referencing System Data
window.ReferenceData = {
	"types" : {
		"book" : {
			"fields" : [
				"title",
				"year",
				"author",
				"publisher"
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
			"list_template" : "'{{title}}' ({{year}}) {{#if website_name}}_{{website_name}}_.{{/if}} Available at: {{url}} (Accessed: {{date_render date_accessed 'DD MMMM YYYY'}})"
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