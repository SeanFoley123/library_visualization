$(function() {
	var width = window.innerWidth,
	    height = window.innerHeight - $('#search-holder').height() - 20;

	var svg = d3.select( "body" )
	      .append( "svg" )
	      .attr( "width", width )
	      .attr( "height", height );

	var highLevel = svg.append("g").attr( "class", "holder");
	// var loadingbar = svg.append("g")
	var spacing = 40;
	var radius = 10;
	var current_selection, current_index;
	var widthAdjusted = width/2;

	function constructTree(levelData) {
		if (typeof levelData == "number") {
			// Do something
			alert(levelData + " books under that category!");
		} else {
			$('.forrest').remove();
			$('.bar').remove();
	    	
	    	highLevel.selectAll('.forrest')
		        .data(Object.keys(levelData))
		        .enter().append("circle")
		        .attr( "class", "forrest" )
		        .attr( "cx", 0)
		        .attr( "r", radius)
		        .attr( "fill", "green")
		        .on("mouseover", function(d){
		            d3.select(this).attr("fill","black");
		            $('#title').text(d).show();
		            $('#title').css("margin-left", "-" + $("#title").width()/2 + "px" );
		        })
		        .on("mouseout", function(d) {
		            d3.select(this).attr("fill", "green");
		            $('#title').hide();
		        })
		        .on("click", function(key, i) {
		        	if (typeof levelData[key] !== "number") {
		        		current_selection = this;
			        	current_index = i;
			        	radius = radius*2;
			        	spacing = radius*4;

			        	widthAdjusted = width/2 - ((Object.keys(levelData[key]).length - 1) * spacing)/2;
				        highLevel.transition().duration(2000).attr("transform", "translate("+ widthAdjusted +","+ (3 * window.innerHeight/4) +")")
		        	}
		        	constructTree(levelData[key]);
		        });

		    current_index = Object.keys(levelData).length/2;

		    highLevel.selectAll('.forrest').transition().duration(2000).attr('r', radius)
			highLevel.selectAll('.forrest').transition().duration(2000).attr("cx", function(d, i){
	        		return (this != current_selection)? spacing * (current_index - i) : 0;
	        	});

		    highLevel.attr("transform", "translate("+ widthAdjusted +","+ (3 * window.innerHeight/4) +")")
		}
	}

	$('form#search').submit(function(event) {
		event.preventDefault();
		radius = 10;
		spacing = 40
		
		var query = $(this).find('input[name="query"]').val();
		// loadingbar.append("rect").attr("width", 140).attr("height", 10).attr("class", "bar").attr("color", "green");
		// loadingbar.attr("transform", "translate(" + (width/2-70) + "," + 70 + ")");
		
		$.post('/search', {'query': query}, function(res) {
			constructTree(JSON.parse(res));
		});

		return false;
	});
});
