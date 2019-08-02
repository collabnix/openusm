
    $(document).ready(function(){

    var socket = io.connect('http://localhost:8010');
    socket.on('channel_console',
        function (data) {
            console.log(data);
            // add comment to list

        var obj = JSON.parse(data);
        
        
        $('#comments').append(obj.message+ " -- "+obj.session_id+"&#13;&#10;");
        
        //$('#comments').append("<li>Hello</li>");
        
		$('#comments').scrollTop($('#comments')[0].scrollHeight)
        console.log("++++ "+obj.submit_date);
        });

        

        });
