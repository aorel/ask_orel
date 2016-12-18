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
                    console.log('swap');
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