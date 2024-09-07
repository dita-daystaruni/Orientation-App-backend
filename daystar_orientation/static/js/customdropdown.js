var selectorfield = document.getElementById(selectorfield)
var selectText = document.getElementById(selectText)
var options = document.getElementsByClassName(options)
for (option of options){
    option.onclick= function(){
        selectText.innerHTML= this.textContent;
    }
}