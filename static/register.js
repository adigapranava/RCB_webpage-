function myTrim(x) {
  return x.replace(/^\s+|\s+$/gm,'');
}

function toggleMenu(){
  let login = document.querySelector('.error');
  login.classList.toggle('active');
}

function toggleMenu2(){
  let varification = document.querySelector('.otp');
  varification.classList.toggle('active');
}

function intonly(input){
	var regx = /[^0-9]/g;
	input.value = input.value.replace(regx, "");
}

function check_otp(){
    var otp = document.getElementById('otp_ip').value;

    var url = "http://127.0.0.1:5000/add_post";
    
    $.post(url, {
      otp: otp,
      email: "new_email",
    },function(data, status) {
      if (data) {
        console.log("varified");
      }
      else{
        console.log("Wrong OTP")
        //noti = document.getElementById("notification_text");
        //noti.innerHTML = "Failed to Post";
      }
    });    
}

function password_inp(input){
	var regx = /[\s]/g;
	input.value = input.value.replace(regx, "");
}

function onPageLoad(){
    toggleMenu2();
    let msg_holder = document.getElementById('msgs');
    let msg = myTrim(msg_holder.innerHTML);
    let msg_reqd = "enter the code"
    var result = msg.localeCompare(msg_reqd);
    if (result==0) {
        toggleMenu2();
    }
    msg_reqd = "invalid OTP"
    var result = msg.localeCompare(msg_reqd);
    if (result==0) {
        toggleMenu2();
    }
    console.log(msg.localeCompare(msg_reqd));
}

window.onload = onPageLoad;