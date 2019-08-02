

	$(document).ready(function(){

		$("#usb").click(function(){
	
			$("#installation_type").hide();
	
		});
	
		$("#local_lun").click(function(){
		
			alert("Clicked");
			$("#installation_type").show();
	
		});

	});

	
	
	function extension() {
		//alert("inside");
		var fname=document.getElementById("isoFile");
		//alert("isofile "+fname.value);
		//alert(fname.value.substr(fname.value.lastIndexOf('.')+1));
		if(fname.value.substr(fname.value.lastIndexOf('.')+1) == "iso")
			return true;
		else 
			{
			alert("Please select only .iso files");
			document.getElementById("isoFile").focus();
			return false;
			}
		//alert(fname.split('.').pop());
		}
	

		function checkradio1() {
			//alert("hi");
		    //var radios = document.getElementsById("local_lun");
		 	document.getElementById("installation_type").style.display = "none"; 
		}
		
		function checkradio2() {
			//alert("hi");
		    //var radios = document.getElementsById("local_lun");
		 	document.getElementById("installation_type").style.display = "block"; 
		}
		


		var sessionid = '{{test}}'

	    $(document).ready(function(){
		
		$('#Download_Section').hide();
		
	    var socket = io.connect('http://100.98.13.53:8010');
	    socket.on('channel_console',
	        function (data) {
	            console.log(data);
	            // add comment to list

	        	var obj = JSON.parse(data);
	        
	        	var tblRow = "<tr>" + "<td>" + obj.submit_date + "</td>" +
	            "<td>" + obj.message + "</td>" + "</tr>"
	            $(tblRow).appendTo("#userdata tbody");
	            
	        
	        	//$('#comments').append(obj.message+ " -- "+obj.session_id+"&#13;&#10;");
	        
	        	//$('#comments').append("<li>Hello</li>");
	        
				$('#comments').scrollTop($('#comments')[0].scrollHeight)
	        	console.log("++++ "+obj.submit_date);
	       });

		socket.on('channel_file_path',
	        function (data) {
	            
	            
	            console.log(data);
	            // add comment to list

	        	var obj = JSON.parse(data);
	       
	        	console.log("++++ "+obj.submit_date);
	       		console.log("Link Address "+obj.message)
	       		alert(obj.message);
	       		


	       		var link = document.getElementById("link");
	       		var aTag = document.createElement('a');
	       		aTag.setAttribute('href',obj.message);
	       		aTag.setAttribute('target',"_blank");
	       		aTag.innerHTML = "Download Link";
	       		link.appendChild(aTag);
	       		
	       		$('#Download_Section').show();
	       		//document.getElementById("link").innerHTML = '<a href="' + obj.message + '">'+Download Link+'</a>';
	   //    		$('#Download_Alerts').append("<a href='www.google.com'>Download Link</a>");
	       		
	       		
	       		
	       		
	       
	       });


	   });
	   
	      


		
		
		
		