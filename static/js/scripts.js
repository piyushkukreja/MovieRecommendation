$(function(){
	$('.add-favourites').click(function(){
		$.ajax({
			url: '/add-favourites',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});