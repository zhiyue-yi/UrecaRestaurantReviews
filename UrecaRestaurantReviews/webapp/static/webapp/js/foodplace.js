$(document).ready(function () {    
    // keep track of foodItemList
    var foodItemList = JSON.parse(document.getElementById('restaurant_menu').textContent);
    for (var i = 0; i < foodItemList.length; i++){
        foodItemList[i].marked = 0;
    }

    // limits the maximum number of food likes/dislikes
    var likeThreshold = 4;
    var dislikeThreshold = 4;

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
        let likeList = [];
        let dislikeList = [];

        $('.foodplace-feedback-like-food > .foodplace-comment-dropdown-box').each(function(){
            if ($(this).val() != 0) { likeList.push($(this).val()); }
        });
        $('.foodplace-feedback-dislike-food > .foodplace-comment-dropdown-box').each(function(){
            if ($(this).val() != 0) { dislikeList.push($(this).val()); }
        });
        
        // let array 
        let arrValidator = [];
        arrValidator.push((validateText(name)) ? 0 : 1);
        arrValidator.push((validateScore(score)) ? 0 : 2);
        arrValidator.push((validateText(comment)) ? 0 : 3);
        arrValidator.push((validateCharacters(name)) ? 0 : 4);
        arrValidator.push((validateLike() && validateDislike() && validateUniqueOption(likeList.concat(dislikeList))) ? 0 : 5);

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
                "feedback" : comment,
                "like" : likeList,
                "dislike" : dislikeList
            }),
            success: function (response) {
                $('#commentToggler').click();
            }, 
            error: function (response){
                // to be completed
            }
        });
    });

    $("#foodplace-continue-view").on("click", function () {
        location.reload();
    });

    $("#likeItem").on("click", function(e){
        e.preventDefault();
        likeThreshold--;
        showFeedbackItemDropdown(e, ".foodplace-feedback-like-food", likeThreshold);
    });

    $("#dislikeItem").on("click", function(e){
        e.preventDefault();
        dislikeThreshold--;
        showFeedbackItemDropdown(e, ".foodplace-feedback-dislike-food", dislikeThreshold);
    });

    $(document).on("change", '.foodplace-comment-dropdown-box', function(e){
        markSelection($(this).children("option:selected").val());
        unmarkSelection();
        refreshDropdown();
    });

    function showFeedbackItemDropdown(e, elemClass, threshold){
        if (threshold >= 0){
            $(elemClass).append(
                '<select class="form-control foodplace-comment-dropdown-box">' +
                '<option value="0">Select Food Item</option>' +
                getRemainingItem() + 
                '</select>'
            );
        }

        if (threshold == 0){
            e.target.remove();
        }
    }

    function markSelection(selected){
        for (var i = 0; i < foodItemList.length; i++){
            if (foodItemList[i].id == selected){
                foodItemList[i].marked = 1;
            }
        }
    }

    function unmarkSelection(){
        var idList = [];
        $('.foodplace-comment-dropdown-box').each(function (){
            var id = $(this).children("option:selected").val();
            if (id != 0){
                idList.push(id);
            }
        });

        for (var i = 0; i < foodItemList.length; i++){
            var id = foodItemList[i].id;
            var flag = false;
            
            for (var j = 0; j < idList.length; j++){
                if (id == idList[j]){ flag = true; }
            }

            if (flag == false){ foodItemList[i].marked = 0; }
        }
    }

    function refreshDropdown(){
        $('.foodplace-comment-dropdown-box').each(function(){
            $(this).children().each(function(){
                if ($(this)[0].selected != true && $(this).val() != 0){
                    $(this).remove();
                }
            });
        
            $(this).append(getRemainingItem());
        });

    }

    function getRemainingItem(){
        var HTMLString = ""
        for (var i = 0; i < foodItemList.length; i++){
            if (foodItemList[i].marked == 0){
                HTMLString += "<option value='" + foodItemList[i].id + "'>" + foodItemList[i].name + "</option>";
            }
        }
        return HTMLString;
    }

    function validateText(text){
        let newText = text.trim();
        return (newText != "") ? true : false;
    }
    
    function validateScore(score){
        return (score > 0) ? true : false;
    }
    
    function validateCharacters(text){
        let expr = text.match(/^[a-zA-Z]{1,20}$/);
        return (expr == null) ? false : true;
    }
    
    function validateLike(){
        var valid = true;
    
        $('.foodplace-feedback-like-food > .foodplace-comment-dropdown-box').each(function(){
            var flag = false;
            for (var i = 0; i < foodItemList.length; i++){
                if (foodItemList[i].id == $(this).val() || $(this).val() == 0){ 
                    flag = true;
                    break; 
                }
            }
            if (flag == false){ valid = false; }
        });
        return valid;
    }
    
    function validateDislike(){
        var valid = true;
    
        $('.foodplace-feedback-dislike-food > .foodplace-comment-dropdown-box').each(function(){
            var flag = false;
            for (var i = 0; i < foodItemList.length; i++){
                if (foodItemList[i].id == $(this).val() || $(this).val() == 0){ 
                    flag = true;
                    break; 
                }
            }
            if (flag == false){ valid = false; }
        });
        return valid;
    }
    
    function validateUniqueOption(arr){
        for (var i = 0; i < arr.length; i++){
            for (var j = i+1; j < arr.length; j++){
                if (arr[i] == arr[j]){ return false; }
            }
        }
        return true;
    }
    
    function displayError(arrError){
        // mapping error
        let error = {
            "1" : "Name must contain characters <br/>",
            "2" : "Score must be at least 1 <br/>",
            "3" : "Comment must contain characters <br/>",
            "4" : "Name must contain at most 20 alpha characters <br/>",
            "5" : "Something went wrong. Please refresh the page. <br/>",
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
});