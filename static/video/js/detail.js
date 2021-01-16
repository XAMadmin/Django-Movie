function messageBtn() {
    var msg = $("#msg").val();
    var movie_id = $("#get_movie_id").val();
    var username = $("#user_role").val();
    data = {
        "comment": msg,
        "movie_id": movie_id,
        "username": username

    };
    $.get("{% url 'video:send_message'%}",data, function(msg){
        msg = JSON.parse(msg);
        if(msg.errno=='0'){
            $("#msg").val("");
            // alert(msg.msgs.comment)
            location.href = "{% url 'video:detail_parse' movie.pk  %}"
    
        }else{
            alert(msg.errmsg)
        }
});
}