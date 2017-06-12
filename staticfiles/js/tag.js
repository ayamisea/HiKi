//add Tag
function addTag()
{
	var newElement = document.createElement("div");
	var tag = document.getElementById("tag")
	var tagValue = document.getElementById("tagValue").value;
	newElement.name = tagValue;
	newElement.innerHTML = "#" + tagValue;
	newElement.classList.add("mr-2");
	newElement.classList.add("h4");
	newElement.style = "display:inline;";
	newElement.setAttribute("onmouseover", ' this.style = "text-decoration:line-through;display:inline;"');
	newElement.setAttribute("onmouseout", ' this.style = "text-decoration:none;display:inline;"');
	newElement.setAttribute("ondblclick", 'this.parentNode.removeChild(this);');
	//最後再使用appendChild加到要加的元素裡
	tag.appendChild(newElement);
	document.getElementById("tagValue").value = "";
}

//Submit tag
$(document).ready(function() {
    $('#DiaryForm').submit(function() {
        var collection = document.getElementById("tag").childNodes;
        var tagNum = collection.length;
        var i;
        var tags = new Array();
        for(i=0;i<tagNum;++i) {
            tags.push(collection[i].name);
        }
        document.getElementById("tags").value = tags;
    });
});