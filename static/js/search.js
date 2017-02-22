$(function() {
	$('form#search').submit(function(event) {
		event.preventDefault();
		var query = $(this).find('input[name="query"]').val();

		$.post('/search', {'query': query}, function(res) {
			var subjects = JSON.parse(res)['SearchResult']['AvailableFacets'][0]['AvailableFacetValues'];
			var subCounts = []
			$.each(subjects, function(i, subjectData) {
				subCounts.push({
					subject: subjectData.Value,
					count: subjectData.Count
				});
			});

			subCounts.sort(function(a, b) {
			    var textA = a.subject.toUpperCase();
			    var textB = b.subject.toUpperCase();
			    return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
			});

			$('ul#books').html('');
			$.each(subCounts, function(i, item) {
				$('ul#books').append('<li>' + item.subject + ' --- ' + item.count + '</li>');
			});
		});

		return false;
	});
});