$(document).ready(function () {
    $("#commentBtn").on("click", function (e) {
        // prevent submission
        e.preventDefault();
        
        // dismiss error view
        dismissError();

        // retrieve information
        let id = $('.foodplace-place-info-form').attr('id');
        let name = $("#txtName").val();
        let comment = $('#txtFeedback').val();
        let score = $('#stars').children('i.fas.fa-star').length;
        let csrftoken = getCookie('csrftoken');
        
        // let array 
        let arrValidator = [];
        arrValidator.push((validateText(name)) ? 0 : 1);
        arrValidator.push((validateScore(score)) ? 0 : 2);
        arrValidator.push((validateText(comment)) ? 0 : 3);

        // check error array
        for (let i = 0; i < arrValidator.length; i++){
            if (arrValidator[i] != 0){
                displayError(arrValidator);
                return;
            }
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // prepare submission of form
        $.ajax({
            type: "POST",
            url: "/webapp/api/comment",
            data: JSON.stringify({
                "id" : id,
                "name" : name,
                "score" : score,
                "feedback" : comment
            }),
            success: function (response) {
                $('#commentToggler').click();
            }, 
            error: function (response){
                // to be completed
            }
        });
    });
    $("#foodplace-continue-view").on("click", function (e) {
        location.reload();
    });
});

function validateText(text){
    let newText = text.trim();
    return (newText != "") ? true : false;
}

function validateScore(score){
    return (score > 0) ? true : false;
}

function displayError(arrError){
    // mapping error
    let error = {
        "1" : "Name must contain characters <br/>",
        "2" : "Score must be at least 1 <br/>",
        "3" : "Comment must contain characters <br/>"
    }
   
    // error view
    let view = "<div id='alert-view' class='alert alert-danger alert-dismissible fade show' role='alert'>" 
                + "<strong>You should check the following field(s) :</strong><br/>"; 

    // traverse array
    for (let i = 0; i < arrError.length; i++){
        if (arrError[i] != 0){
            let strIndex = (i + 1).toString();
            view += error[strIndex];
        }
    }

    view += "<button type='button' class='close foodplace-modal-close' data-dismiss='alert' aria-label='Dismiss'>" + 
            "<span aria-hidden='true'>&times;</span></button></div>";

    // set error view
    $('.foodplace-feedback-form-container').prepend(view);
}

function dismissError(){
    $("#alert-view").remove();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}