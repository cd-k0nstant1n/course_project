// navbar toggling
const navbarShowBtn = document.querySelector('.navbar-show-btn');
const navbarCollapseDiv = document.querySelector('.navbar-collapse');
const navbarHideBtn = document.querySelector('.navbar-hide-btn');

navbarShowBtn.addEventListener('click', function(){
    navbarCollapseDiv.classList.add('navbar-show');
});
navbarHideBtn.addEventListener('click', function(){
    navbarCollapseDiv.classList.remove('navbar-show');
});

// stopping all animation and transition
let resizeTimer;
window.addEventListener('resize', () =>{
    document.body.classList.add('resize-animation-stopper');
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        document.body.classList.remove('resize-animation-stopper');
    }, 400);
});

function validate() {
    var password1 = document.getElementById("pass1").value;
    var password2 = document.getElementById("pass2").value;
    if (password1 != password2) {
      document.getElementById("error").innerHTML = "Passwords do not match.";
      return false;
    } else {
      document.getElementById("error").innerHTML = "";
      return true;
    }
  }

  document.getElementById("appointment").addEventListener("click", function(){
      document.querySelector(".popup").style.display = "flex";
  })

  document.querySelector(".close").addEventListener("click", function(){
      document.querySelector(".popup").style.display = "none";
  })
  document.getElementById('service').addEventListener('change', function() {
    var datetimeFields = document.getElementById('appointment_date');
    if (this.value === "") {
      datetimeFields.classList.add('hidden');
    } else {
      datetimeFields.classList.remove('hidden');
    }
  });
  