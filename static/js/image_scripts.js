<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
	<script>
		var mname = document.getElementById("movie-name").alt;
		// $.ajax({
		// 	type: "GET",
		// 	dataType: "json",
		// 	url: "localhost:5000/movies_images/" + titel,
		// 	success: function (data) {
		// 		console.log(data);
		// 		return $.get(data);
		// 	},
		// 	async: false,
		// 	error: function () {
		// 		return "Image not found.";
		// 	}
		// });
		// var source = getImage();



		// $(document).ready(function(){
		// console.log("loaded");

		// var getData = function(movieTitle){
		// var movieUrl = "http://www.omdbapi.com/?apikey=64a25551&t=" + movieTitle + "&r=json";
		// $.ajax({
		// "url": movieUrl,
		// "method": "GET",
		// success: function(movieUrl) {
		// 	console.log(movieTitle);
		// 	handleResponse(movieUrl);
		// 	},
		// error: function(movieUrl){
		// 	console.log(movieUrl);
		// }
		// });
		// };

		// var addAJAXFunction = function(){
		// 	$('#movie-image').bind('DOMSubtreeModified', function(){
		// 	console.log('changed');
		// 	var movieTitle = document.getElementById("movie-image").alt;
		// 	getData(movieTitle);
		// 	});

		// 	// $(".container").click(function(){
		// 	// var movieTitle = document.getElementById("movie-image").alt;
		// 	// getData(movieTitle);
		// 	// });
		// };



		// var handleResponse = function(data){
		// 	var name = data.Title;
		// 	var imagePath = data.Poster;
		// 	document.getElementById("movie-image").src = imagePath;
		// 	};

		// addAJAXFunction();

		// });









		//console.log($.getJSON("https://api.themoviedb.org/3/discover/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb"));


		

		var getPoster = function () {

			var film = document.getElementById("movie-image").alt;

			if (film == '') {

				$('.movie-item').html(
					'<div class="alert"><strong>Oops!</strong> Try adding something into the search field.</div>');

			} else {

				$.getJSON("https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=" +
					film + "&callback=?",
					function (json) {
						if (json != "Nothing found.") {
							console.log(json);
							$('#movie-image').html('<img src=\"http://image.tmdb.org/t/p/w500/' + json.results[0]
								.poster_path + '\" class=\"img-responsive\" >');
						} else {
							$.getJSON(
								"https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=goonies&callback=?",
								function (json) {

									console.log(json);
									$('.movie-item').html(
										'<div class="alert"><p>We\'re afraid nothing was found for that search.</p></div><p>Perhaps you were looking for The Goonies?</p><img id="thePoster" src="http://image.tmdb.org/t/p/w500/' +
										json[0].poster_path + ' class="img-responsive" />');
								});
						}
					});

			}

			return false;
		}

		$('.container').click(getPoster);
		// $('#term').keyup(function (event) {
		// 	if (event.keyCode == 13) {
		// 		getPoster();
		// 	}
		// });
	</script>