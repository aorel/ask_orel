(function () {

    $('.js-vote').on('click', function(){
        var $btn = $(this)
        var $id = $btn.data('id')
        var $type = $btn.data('type')
        var $token = $('input[name=csrfmiddlewaretoken]').val()
        console.log( $id );

        var $subtype;
        if($type.includes('question-')){
            $subtype = 'question-';
        }
        else if($type.includes('answer-')){
            $subtype = 'answer-';
        }
        else{
            console.log('error');
        }

        $.ajax({
            url: '/vote/',
            method: 'POST',
            data:{
                id: $id,
                type: $type,
                csrfmiddlewaretoken: $token
            }
        }).done( function(resp){
            console.log(resp);
            if(resp && resp.status == 'ok' && 'action' in resp){
                //window.location.reload();

                $('span[data-id='+$id+'][data-type='+$subtype+'votes]').text(resp.action.votes);

                var $btn_like = $('span[data-id='+$id+'][data-type='+$subtype+'like]').parents('.btn');
                var $btn_dislike = $('span[data-id='+$id+'][data-type='+$subtype+'dislike]').parents('.btn');
                if(resp.action.type == 'like'){
                    if(resp.action.change == 2){
                        $btn_like.addClass('askme-btn-like');
                        $btn_dislike.removeClass('askme-btn-dislike');
                    }
                    else if(resp.action.change == 1){
                        $btn_like.addClass('askme-btn-like');
                    }
                    else if(resp.action.change == -1){
                        $btn_like.removeClass('askme-btn-like');
                    }
                    else{
                        console.log('error');
                    }
                }
                else if(resp.action.type == 'dislike'){
                    if(resp.action.change == -2){
                        $btn_dislike.addClass('askme-btn-dislike');
                        $btn_like.removeClass('askme-btn-like');
                    }
                    else if(resp.action.change == -1){
                        $btn_dislike.addClass('askme-btn-dislike');
                    }
                    else if(resp.action.change == 1){
                        $btn_dislike.removeClass('askme-btn-dislike');
                    }
                    else{
                        console.log('error');
                    }
                }
                else{
                    console.log('error in type');
                    // TODO write error on server
                }
            }
            else{
                //alert(resp.status);
                console.log('error status or no action');
                // TODO write error on server
            }
        });
        return false;
    });

    $('.js-correct').on('click', function(){
        var $btn = $(this)
        console.log( $btn.data('id') );

        $.ajax({
            url: '/correct/',
            method: 'POST',
            data:{
                id: $btn.data('id'),
                type: $btn.data('type'),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
        }).done( function(resp){
            console.log(resp);
            if(resp && resp.status == 'ok'){
                window.location.reload();
            }
            else{
                alert(resp.status);
            }
        });
        return false;
    });

    function handle_comet(){
        $.ajax({
            url: '/sub/'+$question_id,
            dataType: 'json'
        }).done( function(resp){

        var $new_answer =
            `
            <div class="answer">
                <div class="media">
                    <div class="media-left">
                        <img src="`+resp.avatar+`" class="media-object img-thumbnail question-avatar">
                    </div>
                    <div class="media-body">
                        <div class="answer-body">
                            `+resp.text+`
                        </div>
                        <div class="askme-meta">
                            <div class="row">
                                <div class="col-md-7">
                                    <p> `+resp.date+` <a href="#">`+resp.user+`</a>
                                </div>
                                <div class="col-md-5 text-right">
                                    Votes <span class="badge askme-badge">`+resp.vote_sum+`</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `

            $( ".answer-form" ).before($new_answer);
            console.log(resp);
            handle_comet();
        });
    }

    //get question id
    //if ok -> pass id in function
    //handle_comet();
    var $question_id;
    var $path = window.location.pathname;
    if($path.includes('/question/')){
        var $parts = $path.split("/");
        $question_id = $parts[2];
        console.log($question_id);

        handle_comet();
        console.log($path);
    }



    var $search_sub_string;
    var $search_sub_string_refresh_flag;

    var $search_request_run;

    var $search_list = $("#askme-search-div ul");
    var $token = $('input[name=csrfmiddlewaretoken]').val()
    $('#askme-search').on('focus', function(){
        //$('#askme-search-div').css('display', 'block');

        $search_request_run = true;
        search_request();
    });
    $('#askme-search').on('focusout', function(){
        //$('#askme-search-div').css('display', 'none');

        $search_request_run = false;
    });
    $('#askme-search').on('keyup', function(){
        $search_sub_string = $(this).val();
        $search_sub_string_refresh_flag = true;
    });

    function search_request(){
        console.log("time: " + $search_sub_string);

        if($search_sub_string_refresh_flag){
            if($search_sub_string){
                console.log("ajax: " + $search_sub_string);

                $.ajax({
                    'url': '/search/',
                    'method': 'POST',
                    data:{
                        'sub_string': $search_sub_string,
                        'csrfmiddlewaretoken': $token
                    }
                }).done( function(resp){
                    console.log(resp.matching);
                    $search_list.empty();
                    if(resp.matching.length == 0){
                        $('#askme-search-div').css('display', 'none');
                    }
                    else{
                        $('#askme-search-div').css('display', 'block');
                        for (i = 0, len = resp.matching.length; i < len; i++){
                            $search_list.append('<li><a href="#">'+resp.matching[i]+'</a></li>');
                        }
                    }
                });
            }
            else{
                $('#askme-search-div').css('display', 'none');
            }
        }

        $search_sub_string_refresh_flag = false;
        if($search_request_run){
            setTimeout(function() { search_request(); }, 1000);
        }
    }

})();