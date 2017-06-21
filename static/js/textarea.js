//textarea auto resize
var textareaSize = function() {
	var textarea = document.getElementById('textarea');
	setTimeout(function(){
		textarea.style.height = 'auto';
		textarea.style.height = textarea.scrollHeight + 'px';
		},0);
}
window.addEventListener('load', textareaSize , false);
window.addEventListener('keydown', textareaSize , false);
