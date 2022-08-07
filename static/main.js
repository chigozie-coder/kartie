const multiColors = a =>{
  let c = a.color
  let el = document.querySelectorAll(a.el)[a.n]
  let elm = el.innerText
  el.innerText = ''
  if (c.length == elm.length){
    for (var i = 0; i < elm.length; i++) {
      el.innerHTML += `<span style='color:${c[i]}'>${elm[i]}</span>`
    }
  }
  else{
    throw Error("Length of text must be equal to length of array")
  }
}
var colors = ["red","darkorange","darkorange","deeppink","deeppink","red"]

var logo_count = document.querySelectorAll(".logo")
for (var i = 0; i < logo_count.length; i++) {
  multiColors({
  el: '.logo',
  n: i,
  color: colors
})
}
let slideIndex = 0;


function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 3500)
}
var isOpen= false
function onav(){ 
/*is sidebar is not open ,then open it*/
if(!isOpen)
  {
        if (navigator.vibrate) {
          navigator.vibrate(50)
        }
        document.getElementById('side_bar').
        style.transform="translateX(0px)"; 
        isOpen=true
        
  }
else
  {
    if (navigator.vibrate) {
          navigator.vibrate(50)
    }
   document.getElementById('side_bar').
   style.transform="translateX(-100vw)";
   isOpen=false
  }
}
function cnav(){
    if (navigator.vibrate) {
          navigator.vibrate(50)
    }
   document.getElementById('side_bar').
   style.transform="translateX(-100vw)";
   isOpen=false
}
function greetUser() {
         var time = new Date().getHours();
         if (time < 11) {
            return "Good morning";
         } else if (time < 18) {
            return "Good day";
         } else {
            return "Good evening";
         }
      }
      
      document.getElementById("greet_day").innerHTML = greetUser();