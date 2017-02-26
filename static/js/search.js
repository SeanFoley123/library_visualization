$(function() {
	var width = window.innerWidth,
	    height = window.innerHeight - $('#search-holder').height() - 20;

	var svg = d3.select( "body" )
	      .append( "svg" )
	      .attr( "width", width )
	      .attr( "height", height );
	    
	var highLevel = svg.append("g")
	var loadingbar = svg.append("g")
	var spacing = 40;
	var radius = 10;
	highLevel.attr("transform", "translate("+ 0+","+ height/2 +")")
	function constructTree(levelData) {
		if (typeof levelData == "number") {
			console.log(levelData);
		} else {
			$('.forrest').remove();
			$('.bar').remove();

	    	highLevel.selectAll('.forrest')
		        .data(Object.keys(levelData))
		        .enter().append("circle")
		        .attr( "class", "forrest" )
		        .attr( "cx", function(d, i) {return (width/2 - (spacing*(Object.keys(levelData).length-1)/2)) + spacing*i})
		        .attr( "r", radius)
		        .on("mouseover", function(d){
		            d3.select(this).attr("fill","red");
		            $('#title').text(d).show();
		            $('#title').css("margin-left", "-" + $("#title").width()/2 + "px" );
		        })
		        .on("mouseout", function(d){
		            d3.select(this).attr("fill","black");
		            $('#title').hide();
		        })
		        .on("click", function(key, i) {
		        	var current_selection = this;
		        	var current_index = i;
		        	radius = radius*2;
		        	spacing = radius*4
		        	// console.log()
		        	highLevel.selectAll('.forrest').filter(function(d, i) {return i != current_index})
		        		.transition().duration(2000).remove()
		        		.attr("cx", function(d, i){
		        			return (current_index > i) ? -100:width+100;})
		        		.attr('r', radius);
		        	if (typeof levelData[key] == 'object'){
		        		highLevel.selectAll('.tree').data(Object.keys(levelData[key]))
		        		.enter().append('circle').attr('class', 'tree').attr('cx', d3.select(current_selection).attr('cx')) //d3.selectAll(current_selection)
		        		.attr('r', radius/2);
		        		var selection_size = Object.keys(levelData[key]).length;
		        	}
		        	d3.select(current_selection).remove();
		        	var final_trans = highLevel.selectAll('.tree').transition().duration(2000).attr('cx', function (d, i){
		        		return width/2 - (spacing*(Object.keys(levelData[key]).length-1)/2) + spacing*i;
		        	}).attr('r', radius);

		        	var call_next = final_trans.transition().each('end', function (d, i) {
		        		if (i > selection_size-1) {
		        		constructTree(levelData[key]);}
		        	}).remove();
	        	
		        });
		        // .each('end', constructTree(levelData[key]))
		    // var widthAdjusted = (window.innerWidth/2 - (spacing * (Object.keys(levelData).length)/2) + radius*2);
		}
	}

	$('form#search').submit(function(event) {
		event.preventDefault();
		radius = 10;
		spacing = 40
		var query = $(this).find('input[name="query"]').val();
		loadingbar.append("rect").attr("width", 140).attr("height", 10).attr("class", "bar").attr("color", "green");
		loadingbar.attr("transform", "translate(" + (width/2-70) + "," + 70 + ")");
		$.post('/search', {'query': query}, function(res) {
			constructTree(JSON.parse(res));
		});

		return false;
	});
});
