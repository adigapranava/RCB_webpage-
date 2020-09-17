//global variable
var p_id = 0;
var is_postable = false;

function toggleMenu(){
  $(".notification").hide();
}

function showPreview(event){
  if(event.target.files.length > 0){
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    is_postable = true;
  }
  else{
    var preview = document.getElementById("file-ip-1-preview");
    var src = document.getElementById('file-ip-1-preview').src;
    toDataURL(src, function(dataUrl) {
      preview.src = dataUrl;
    });
    is_postable = false;
  }
}

function toggle_open()
{
  $(".posting").show();
}

function toggle_close()
{
  $(".posting").hide();
  is_postable = false;
}

function previous_post(){
  console.log("previous_post")
  --p_id;
  get_post()
}

function next_post(){
  console.log("next_post")
  ++p_id;
  get_post()
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

function get_new_post(){
  p_id =0;
  get_post()
}

function add_post() {
  if (is_postable) {
    console.log( "Posting" );

    var src = document.getElementById('file-ip-1-preview').src;
    toDataURL(src, function(dataUrl) {
    var url = "http://127.0.0.1:5000/add_post";
    
    $.post(url, {
      name: "hai",
      email: "new_email",
      profile: dataUrl
    },function(data, status) {
      if (data) {
        console.log("posted");
        noti = document.getElementById("notification_text");
        noti.innerHTML = "Posted Successfully";
        $(".notification").show();
        $(".posting").hide();
        get_new_post();
      }
      else{
        noti = document.getElementById("notification_text");
        noti.innerHTML = "Failed to Post";
        $(".notification").show();
        $(".posting").hide();
      }
    });    
    });
    is_postable = false;
  }
}

function get_post(){
  var url = "http://127.0.0.1:5000/get_post";
  $.post(url, {
      p_idx: p_id,
    },function(data, status) {
      console.log("got response for get_post request");
      console.log(p_id);
      if(data) {
          console.log( "document loaded" );
          var preview = document.getElementById("file-post-2-preview");
          preview.src = data.post;
          var name = document.getElementById("name-post-1-preview");
          name.innerHTML = data.name;
          var dp = document.getElementById("file-post-1-preview");
          dp.src = data.dp;
          console.log("p_id", data.post_id)
      }
  });
}

function onPageLoad() {
  $(".posting").hide();
  $(".notification").hide();
  var url = "http://127.0.0.1:5000/give_details";
  $.get(url,function(data, status) {
      console.log("got response for give_details request");
      if(data) {
          console.log( "document loaded" );
          var preview = document.getElementById("file-ip-2-preview");
          preview.src = data.pic;
          var name = document.getElementById("profile_name");
          name.innerHTML = data.name;
      }
  });
  get_post()
}

window.onload = onPageLoad;