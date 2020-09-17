function toggleMenu(){
  //let login = document.querySelector('.error');
  //login.classList.toggle('active');
  $(".notification").hide();
}

function showPreview(event){
  if(event.target.files.length > 0){
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
  }
  else{
    var preview = document.getElementById("file-ip-1-preview");
    var src = document.getElementById('file-ip-1-preview').src;
    toDataURL(src, function(dataUrl) {
      preview.src = dataUrl;
    });
  }
}

function toDataURL(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function() {
    var reader = new FileReader();
    reader.onloadend = function() {
      callback(reader.result);
    }
    reader.readAsDataURL(xhr.response);
  };
  xhr.open('GET', url);
  xhr.responseType = 'blob';
  xhr.send();
}


function save_to_db() {
  console.log( "Saving To Database" );
  new_name = document.getElementById('profile_name').value
  new_email = document.getElementById('profile_email').value

  var src = document.getElementById('file-ip-1-preview').src;
  toDataURL(src, function(dataUrl) {
    var url = "http://127.0.0.1:5000/update_details";
    
    $.post(url, {
      name: new_name,
      email: new_email,
      profile: dataUrl
  },function(data, status) {});
  console.log('Saved To Database');
});
  $(".notification").show();
}

function onPageLoad() {
  var url = "http://127.0.0.1:5000/give_details";
  $(".notification").hide();
  $.get(url,function(data, status) {
      console.log("got response for give_details request");
      if(data) {
          console.log( data );
          var preview = document.getElementById("file-ip-1-preview");
          preview.src = data.pic;
          var name = document.getElementById("profile_name");
          name.value = data.name;
          var email = document.getElementById("profile_email")
          email.value = data.email;
      }
  });
}

window.onload = onPageLoad;