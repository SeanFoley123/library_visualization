$(function() {
	var width = window.innerWidth,
	    height = window.innerHeight - $('#search-holder').height() - 20;

	var svg = d3.select( "body" )
	      .append( "svg" )
	      .attr( "width", width )
	      .attr( "height", height );
	    
	var highLevel = svg.append("g")
	var spacing = 40;
	var radius = 10;

	function constructTree(levelData) {
		if (typeof levelData == "number") {
			console.log(data);
		} else {
			$('.forrest').remove();

	    	highLevel.selectAll('.forrest')
		        .data(Object.keys(levelData))
		        .enter().append("circle")
		        .attr( "class", "forrest" )
		        .attr( "cx", function(d, i) { return i * spacing })
		        .attr( "r", function(d) { return radius })
		        .on("mouseover", function(d){
		            d3.select(this).attr("fill","red");
		            $('#title').text(d).show();
		            console.log($("#title").width());
		            $('#title').css("margin-left", "-" + $("#title").width()/2 + "px" );
		        })
		        .on("mouseout", function(d){
		            d3.select(this).attr("fill","black");
		            $('#title').hide();
		        })
		        .on("click", function(key) {
		        	constructTree(levelData[key])
		        });

		    var widthAdjusted = (window.innerWidth/2 - (spacing * (Object.keys(levelData).length)/2) + radius*2);
		    highLevel.attr("transform", "translate("+ widthAdjusted +","+ window.innerHeight/2 +")")
		}
	}

	$('form#search').submit(function(event) {
		event.preventDefault();
		var query = $(this).find('input[name="query"]').val();

		$.post('/search', {'query': query}, function(res) {
			constructTree(JSON.parse(res));
		});

		return false;
	});
});
