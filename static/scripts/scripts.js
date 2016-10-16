$(document).ready(function() {
	console.log('asdfadsf');
	$('#openAddInfo').click(function() {
		console.log('display!');
		$('#addInfoForm').css('display', 'inline-block');
	});
	$('#doItLater').click(function() {
		console.log('do it later -- close the browser, return a value');
	});
});