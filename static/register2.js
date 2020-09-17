function close_noti() {
  $(".notification2").hide();
}

function notify(msg){
  noti = document.getElementById('msgs');
  noti.innerHTML = msg.toString();
  $(".notification2").show();
}

function toggleMenue(){
  window.location.href = "http://127.0.0.1:5000/home";
}

function toggleMenu2(){
  $('.otp').hide();
}

function nospace(input){
  var regx = /[\s]/g;
  input.value = input.value.replace(regx, "");
}

function intonly(input){
  var regx = /[^0-9]/g;
  input.value = input.value.replace(regx, "");
}

function send_otp(){
  if(document.getElementById("form").checkValidity()){
        email = document.getElementById('email_holder').value;
        password = document.getElementById('password_holder').value;
        age = document.getElementById('age_holder').value;
        console.log(email,password,age);

        var url = "http://127.0.0.1:5000/register";

        $.post(url, {
          email: email,
          password: password,
          age: age
        },function(data, status) {
          if (data) {
            if (data.status) {
              $('.otp').show();
              notify("OTP sent again");
            } else {
              if (data.redirect) {
                window.location.href = "http://127.0.0.1:5000/login";
              }
              else{
                notify(data.msg);
              }
            }
          }
          else{
            console.log("Wrong..")
          }
        });    
      }
}



function check_otp(){
  if(document.getElementById("otp_ip").checkValidity()){
    email = document.getElementById('email_holder').value;
    password = document.getElementById('password_holder').value;
    age = document.getElementById('age_holder').value;
    OTP = document.getElementById('otp_ip').value;

    var url = "http://127.0.0.1:5000/check_otp";

        $.post(url, {
          email: email,
          password: password,
          age: age,
          otp: OTP
        },function(data, status) {
          if (data) {
            if (data.status) {
              window.location.href = "http://127.0.0.1:5000/home";
            }
            else{
                notify(data.msg);
            }
          }
        });

  }
}

function onPageLoad(){
    close_noti();
    toggleMenu2();
    document.getElementById("submit_form").addEventListener("click", function(event) {
      event.preventDefault();
      if(document.getElementById("form").checkValidity()){
        email = document.getElementById('email_holder').value;
        password = document.getElementById('password_holder').value;
        age = document.getElementById('age_holder').value;
        console.log(email,password,age);

        var url = "http://127.0.0.1:5000/register";

        $.post(url, {
          email: email,
          password: password,
          age: age
        },function(data, status) {
          if (data) {
            if (data.status) {
              $('.otp').show();
              notify(data.msg);
            } else {
              if (data.redirect) {
                window.location.href = "http://127.0.0.1:5000/login";
              }
              else{
                notify(data.msg);
              }
            }
          }
          else{
            console.log("Wrong..")
          }
        });    
      }
      else{
        notify("please enter correct/ all fields");
      }
    }); 

    
}

window.onload = onPageLoad;