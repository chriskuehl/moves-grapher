google.load("visualization", "1", {packages:["corechart"]}); // Google Charts

$(document).ready(function() {
	// load data
	$.get("records.cgi", function(records) {
		records.unshift(["Date", "Miles Walked"]);
		var data = google.visualization.arrayToDataTable(records);
		var options = {
			vAxis: {title: "Miles"},
			hAxis: {title: "Date"},
			legend: {position: "none"},
			chartArea: {left: 40, top: 40, width: "100%", height: "70%"}
		};

		var chart = new google.visualization.SteppedAreaChart(document.getElementById("chart"));
		chart.draw(data, options);
	});
});
