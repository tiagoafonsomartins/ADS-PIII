//create Tabulator on DOM element with id "example-table"
var headers;

//var csv is the CSV file with headers
function csvJSON(){
	var csv = document.getElementById("myFile").files[0];
	const reader = new FileReader();

	reader.onload = function (e) {
		const text = e.target.result;
		const data = csvToArray(text);
		json_data = JSON.stringify(data);
		var my_columns = []; // create an empty array
		for(let i = 0; i < headers.length; i++) {
			my_columns.push({
				title: headers[i],
				field: headers[i],
				width: 150
			});
			console.log(my_columns[i]);
		}
		var table = new Tabulator("#csv_table", {
		height:400, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
		//assign data to table
		data:json_data,
		layout:"fitColumns", //fit columns to width of table (optional)
		columns: my_columns, //Define Table Columns
		});
	};
	reader.readAsText(csv);
}


// This will parse a delimited string into an array of
// arrays. The default delimiter is the comma, but this
// can be overriden in the second argument.
function csvToArray( strData, strDelimiter ){
	// Check to see if the delimiter is defined. If not,
	// then default to comma.
	strDelimiter = (strDelimiter || ",");

	// Create a regular expression to parse the CSV values.
	var objPattern = new RegExp(
		(
			// Delimiters.
			"(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

			// Quoted fields.
			"(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

			// Standard fields.
			"([^\"\\" + strDelimiter + "\\r\\n]*))"
		),
		"gi"
		);
	// Create an array to hold our data. Give the array
	// a default empty first row.
	var arrData = [[]];
	// Create an array to hold our individual pattern
	// matching groups.
	var arrMatches = null;
	// Keep looping over the regular expression matches
	// until we can no longer find a match.
	while (arrMatches = objPattern.exec( strData )){
		// Get the delimiter that was found.
		var strMatchedDelimiter = arrMatches[ 1 ];
		// Check to see if the given delimiter has a length
		// (is not the start of string) and if it matches
		// field delimiter. If id does not, then we know
		// that this delimiter is a row delimiter.
		if (
			strMatchedDelimiter.length &&
			(strMatchedDelimiter != strDelimiter)
			){
			// Since we have reached a new row of data,
			// add an empty row to our data array.
			arrData.push( [] );
		}
		// Now that we have our delimiter out of the way,
		// let's check to see which kind of value we
		// captured (quoted or unquoted).
		if (arrMatches[ 2 ]){
			// We found a quoted value. When we capture
			// this value, unescape any double quotes.
			var strMatchedValue = arrMatches[ 2 ].replace(
				new RegExp( "\"\"", "g" ),
				"\""
				);
		} else {
			// We found a non-quoted value.
			var strMatchedValue = arrMatches[ 3 ];
		}

		// Now that we have our value string, let's add
		// it to the data array.
		arrData[ arrData.length - 1 ].push( strMatchedValue );
	}

	//Now that the information is parsed correctly we can send it to the tabulator table
	var result = [];
	headers=arrData[0];

	for(var i=1;i<arrData.length;i++){

	  var obj = {};
	  //var currentline=lines[i].split(/('",'+|','+)/g);

	  for(var j=0;j<headers.length;j++){
		  obj[headers[j]] = arrData[i][j];
	  }
	  result.push(obj);
	}
	// Return the parsed data.
	return( result );
}
	
	
//If Yes pressed -> Show all fields. If No -> Hide and allow them to be empty when submitting
function yesnoCheck() {
	var divsToHide = document.getElementsByClassName("ifChecked");
	if (document.getElementById('yes_changes').checked) {
		for(var i = 0; i < divsToHide.length; i++){
			divsToHide[i].style.visibility = "visible";
			divsToHide[i].style.required = 'true';
		}
	} else {
		for(var i = 0; i < divsToHide.length; i++){
			divsToHide[i].style.visibility = "hidden";
			divsToHide[i].style.required = 'false';
		}

	}
};
