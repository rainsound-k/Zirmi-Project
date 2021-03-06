function commentAdd (pk, is_auth, url, csrf_token, next_path) {
  var content = $("#addComment-"+pk+">input").val();
  if (content && is_auth == "True") {
    $.ajax({
      type: "POST",
      url: url,
      data: {
        'pk': pk,
        'content': content,
        'next_path': next_path,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: "html",

      success: function(data, textStatus, jqXHR) {
        $("#addComment-"+pk+">input").val("");
        $("#comment-box").load(window.location + " #comment-box");
      },
      error: function(request, status, error) {
        alert("잘못된 접근입니다");
        console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      }
    });
  } else if (content && is_auth == "False") {
    alert("로그인이 필요합니다");
    window.location.replace("/login/?next="+next_path);
  } else {
    alert("댓글 내용을 입력해주세요")
  };
}

function commentDel (pk, url, csrf_token, count) {
  $.ajax({
    type: "POST",
    url: url,
    data: {
      'pk': pk,
      'csrfmiddlewaretoken': csrf_token
    },
    dataType: "json",

    success: function(response) {
      if(response.status){
        $("#comment-"+pk).remove();
        $(count).load(window.location + " " + count);
      }
    },
    error: function(request, status, error) {
      alert("잘못된 접근입니다")
      console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    }
  });
}

function replyAddForm (pk) {
  if ($("#replyAddContainer-"+pk).css("display") == "none") {
    $("#comment-"+pk).children('.comment-content').last().removeClass("border-bottom");
    $("#replyAddContainer-"+pk).slideToggle(200);
    $("#addReply-"+pk+"> input").focus();
  } else {
    $("#replyAddContainer-"+pk).slideToggle(200);
    $("#comment-"+pk).children('.comment-content').last().addClass("border-bottom");
  };
}

function replyAdd (parent_pk, pk, is_auth, url, csrf_token, next_path) {
  var content = $("#addReply-"+parent_pk+">input").val();
  if (content && is_auth == "True") {
    $.ajax({
      type: "POST",
      url: url,
      data: {
        'pk': pk,
        'parent_pk': parent_pk,
        'content': content,
        'next_path': next_path,
        'csrfmiddlewaretoken': csrf_token
      },
      dataType: "html",

      success: function(data, textStatus, jqXHR) {
        $("#addReply-"+parent_pk+">input").val("");
        $("#comment-box").load(window.location + " #comment-box");
      },
      error: function(request, status, error) {
        alert("잘못된 접근입니다");
        console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      }
    });
  } else if (content && is_auth == "False") {
    alert("로그인이 필요합니다");
    window.location.replace("/login/?next="+next_path);
  } else {
    alert("댓글 내용을 입력해주세요")
  };
}

function replyDel (pk, url, csrf_token, count) {
  $.ajax({
    type: "POST",
    url: url,
    data: {
      'pk': pk,
      'csrfmiddlewaretoken': csrf_token
    },
    dataType: "json",

    success: function(response) {
      if(response.status){
        $("#replyComment-"+pk).remove();
        $(count).load(window.location + " " + count);
      }
    },
    error: function(request, status, error) {
      alert("잘못된 접근입니다")
      console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
    }
  });
}
