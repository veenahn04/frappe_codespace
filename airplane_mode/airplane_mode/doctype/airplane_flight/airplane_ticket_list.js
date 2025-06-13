frappe.listview_settings["Airplane Flight"] = {
add_fields:["source_airport_code","status"],
get_indicator: function (doc) {
		var indicator = [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
        if (doc.status == "Booked") {
			indicator[1] = "grey";
		}
		return indicator;
	},
}