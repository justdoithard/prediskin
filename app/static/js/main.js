document.addEventListener("DOMContentLoaded", () => {
    var owl = $('.owl-carousel');
    owl.owlCarousel({
      margin: 10,
      nav: true,
      loop: true,
      responsive: {
        0: {
          items: 1
        },
        600: {
          items: 2
        },
        1000: {
          items: 3
        }
      }
    })
  })

function filterSelection(c) {
  var x, i, m;
  m = document.getElementById("sec3");
  x = document.getElementsByClassName("filterDiv");
  for (i = 0; i < x.length; i++) {
    x[i].style.display='none';
    x[i].classList.remove('active');
    if (x[i].className.indexOf(c) > -1){
      x[i].classList.add('active');
      x[i].style.display='flex';
    }
  }
}

// // Add active class to the current button (highlight it)
var header = document.getElementById("btn-toolbar1");
var btns = header.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
  var current = document.getElementsByClassName("btn-default active");
  if (current.length > 0) { 
    current[0].className = current[0].className.replace(" active", "");
     }
     this.className += " active";
  });
}

const button_filter_alphabet = document.getElementById("Penyakit A-Z")
const button_filter_keluhan = document.getElementById("Berdasarkan Keluhan")
// let btnReset = document.querySelector('#reset');
let inputs=document.querySelectorAll('input');

var y = document.getElementById("searchspace");
var x = document.getElementById("btn-toolbar1");

button_filter_alphabet.addEventListener('click', () => {
  // inputs.forEach(input=>input.value='');
  searchFunction(inputs.forEach(input=>input.value=''));
  // console.log('masuk');
  filterSelection("letter-all");
  if (button_filter_keluhan.classList.contains('active')) {
    button_filter_keluhan.classList.remove('active');
    y.style.display = 'none';
  }
  button_filter_alphabet.classList.add('active');
  x.style.display = 'block';
})

button_filter_keluhan.addEventListener('click', () => {
  filterSelection("letter-all");
  if (button_filter_alphabet.classList.contains('active')) {
    button_filter_alphabet.classList.remove('active');
    x.style.display = 'none';
  }
  button_filter_keluhan.classList.add('active');
  y.style.display = 'block';
})

function searchFunction() {
  var input, filter, curr, a, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  curr = document.getElementsByClassName("cont");
  for (i = 0; i < curr.length; i++) {
      a = curr[i].getElementsByClassName("diseaseList")[0];
      console.log(a)
      txtValue = a.value
      console.log(txtValue)
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        curr[i].style.display='block';
      }else{
        curr[i].style.display='none';
      }
  }
}

function alphabetHide() {
  var input, filter, curr, a, i, txtValue, ini;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  curr = document.getElementsByClassName("alphabet");
  for (i = 0; i < curr.length; i++) {
      // a = curr[i].getElementsByTagName("a")[0];
      ini = curr[i].id;
      if (ini.toUpperCase().indexOf(filter) > -1) {
        curr[i].style.display='block';
      }else{
        curr[i].style.display='none';
      }
  }
}
