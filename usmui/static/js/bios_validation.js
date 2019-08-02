
function loadAgain() {
  var xhttp1 = new XMLHttpRequest();
  xhttp1.onreadystatechange = function() {
    if (xhttp1.readyState == 4 && xhttp1.status == 200) {
  
    alert("m back in");
    //document.getElementById("results1").innerHTML = "";
    
   		//document.getElementById("results1").innerHTML = "";
      //document.getElementById("demo").innerHTML = xhttp1.responseText;
      
       //var file_name=document.getElementById("demo").innerHTML;
  //alert(file_name);
  document.getElementById("table").style.display = "none"; 
    document.getElementById("hideform").style.display="none";
       document.getElementById("results").style.display = "none";
        document.getElementById("b1").style.display = "none";
         //document.getElementById("submit").style.display = "none";
     
		//func1();
    }
  }
  var h=document.getElementById("s1").value;
  //alert(h);
   var file_name=document.getElementById("demo").innerHTML;
 // alert(file_name);
   xhttp1.open("GET", "/bios_app/bios_change/?h="+h+"&file_name="+file_name, false);	 
  xhttp1.send();
}


function loadDoc() {
 document.getElementById("hideform").style.display="none";
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
   document.getElementById("results").innerHTML = "";
      document.getElementById("demo").innerHTML = xhttp.responseText;
       document.getElementById("table").style.display = "block"; 
      document.getElementById("b1").style.display = "block"; 
        document.getElementById("s").style.display = "block"; 
          document.getElementById("s1").style.display = "block"; 
         // document.getElementById("submit").style.display = "block";
      
		func();
	
    }
  }
    ipadd=document.getElementById("ipadd").value;
    username=document.getElementById("username").value;
    password=document.getElementById("password").value;

  //alert(password);
	 //xhttp.open("GET", "/bios_return/?username="+username+"&password="+password, false);
 xhttp.open("GET", "/bios_app/bios_return/?ipadd="+ipadd+"&username="+username+"&password="+password, false);
  xhttp.send();
}


var text;
function loadJSON(callback){
	//('<img src="myfolder/' + myphoto + '" />')'
	var hr = new XMLHttpRequest();
	//url='"/static/json/' + x + '"';
	//url='"/static/json/' + x.value + '"';
	//url="/static/json/ + x + ";
	//url="/static/json/ + x.value + ";
	//url="/static/json/"+x;
	//url="/static/json/"+x.value;
	//var path = "/static\/json";
	//var x = "/";
	//var a= "abc.json";
	//var url=path + x+ a;
	//var url="/static/json/abc.json";
	var path = "/static\/json";
		var x = "/";
		var a= document.getElementById("demo").innerHTML;
		alert(a);
		var url=path + x+ a
	
	//console.log(path+x);
	//url=path.join('/static', 'json', 'abc.json')
	hr.open("GET", url, true);
	//hr.open("GET", "/static/json/abc.json", true);

	hr.setRequestHeader("Content-type", "application/json", false);
	hr.onreadystatechange=function() {
		if(hr.readyState == 4 && hr.status == 200) {
		callback(hr.responseText);
		}
		
	};
	hr.send(null);
}





function func() {

loadJSON(function(response) {
		// Parse JSON string into object
  		var data1 = JSON.parse(response);
		
		alert(data1["BIOS"][0]["current_val"]);
		var results= document.getElementById("results");
		var data = ["SERIAL","BIOS CURRENT STATUS", "ATTRIBUTE", "ACTION"] 
	  	text = data1;
		tablearea = document.getElementById('results');
		//tablearea.removeChild(table);
		table = document.createElement('table');
		table.id="mytable";
		$(table).addClass("table table-striped table-bordered bootstrap-datatable datatable");
    	thead = document.createElement('thead');
		tr = document.createElement('tr');
		
		for (var i = 0; i < data.length; i++) {
			var headerTxt = document.createTextNode(data[i]);
			$(headerTxt).addClass("center");
			th = document.createElement('th');
			th.appendChild(headerTxt);
			$(th).addClass("center");
			tr.appendChild(th);
			thead.appendChild(tr);
  			  }
	
		table.appendChild(thead);
		for(i = 0; i < text.BIOS.length; i++) {
		tr = document.createElement('tr');
		td=document.createElement('td');
		$("td").addClass("center");
		tr.appendChild(td);
		td=document.createElement('td');
		tr.appendChild(td);
		td=document.createElement('td');
		tr.appendChild(td);
		td=document.createElement('td');
    	$("td").addClass("center");
		tr.appendChild(td); //Added for checkg box
		var selectList = document.createElement("select");
		selectList.id= "abc"+i;
		

		
		if(!(text.BIOS[i].possible_val[0]))
		{
		var option1 = document.createElement("option");
		var node = document.createTextNode("NA")
		option1.appendChild(node);
		selectList.appendChild(option1);
		
		}
		
		else
		{
		var option1 = document.createElement("option");
		var node = document.createTextNode(text.BIOS[i].possible_val[0])
		option1.appendChild(node);
		
		var option2 = document.createElement("option");
		var node = document.createTextNode(text.BIOS[i].possible_val[1])
		option2.appendChild(node);
		selectList.appendChild(option1);
		selectList.appendChild(option2);
		if(text.BIOS[i].possible_val[0] == (text.BIOS[i].current_val))
			option1.selected="true";
		else
			option2.selected="true";
				
		}
		
				
		//option1.text=text.BIOS[i].possible_val[0]);
		//option2.text=text.BIOS[i].possible_val[1]);
		//option1.text="hey";
		//option2.text="hey";
				
		
       // var checkbox = document.createElement("INPUT"); //Added for checkbox
        //checkbox.type = "checkbox"; //Added for checkbox
		//checkbox.name = "abc"+i;
		//checkbox.id = "abc"+i;
		
		//checkbox.disabled="disabled";
		//checkbox.style="display:none";
		//$("checkbox").addClass("checkbx");
		tr.cells[0].appendChild(document.createTextNode(i+1));
		if(!(text.BIOS[i].current_val))
		
			tr.cells[1].appendChild(document.createTextNode("NA"));
		else
			tr.cells[1].appendChild(document.createTextNode(text.BIOS[i].current_val));
        tr.cells[2].appendChild(document.createTextNode(text.BIOS[i].attribute));
      
        //tr.cells[3].appendChild(checkbox); //Added for checkbox
        tr.cells[3].appendChild(selectList); //Added for checkbox
		table.appendChild(tr);
    }
		tablearea.appendChild(table);
		
		
		 });}

	function validatecheck(h)
	{	//alert("inside valid");
		var x=[];
		for (i=0;i<text.BIOS.length;i++) 
			{
				//alert("inside validate");
				var e = document.getElementById("abc"+i);
				//alert("inside validate1");
				var opt = e.options[e.selectedIndex].value;
				//alert(i);
				//alert(opt);
				//alert("inside validate2");
				var cur_val = document.getElementById("mytable").rows[i+1].cells[1].innerHTML;
				//alert(cur_val);
				//alert("inside validate3");
				//alert("inside validate");
				if (cur_val == opt)
					x[i]=0;
				else
					x[i]=1
				
			}
		h.value=x;
	
	alert("Your selection has been validated, please continue your submission.");
	loadAgain();
	}


	function ipadd_match()
	{
	document.getElementById("mybtn").disabled = true;
	var ipadd=document.getElementById("ipadd");
	pattern="^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	
	if(ipadd.value.match(pattern))
		{
		//var username=document.getElementById("username");
		document.getElementById("username").focus();
		return true;
		}
	else
		{
		alert("please match");
		document.getElementById("ipadd").focus();
		}
	}
	
	function username_match()
	{
	//var password=document.getElementById("password");
	var username=document.getElementById("username");
	
	if(username.value.length == 0)
		{
		alert("provide username");
		document.getElementById("username").focus();
		}
		
	else
		{	if(username.value == "root")
			{
			document.getElementById("password").focus();
			document.getElementById("mybtn").disabled = false;
			return true;
			}
			
			else	
				{
				alert("invalid username");
				document.getElementById("username").focus();
				}
			
		}
	}
	
	function password_match()
	{
	
	var password=document.getElementById("password");
	
	if(password.value.length == 0)
	{
		alert("provide password");
		document.getElementById("password").focus();
	}
		
	else
					
		return true;
	}
	
	

	


	    $(function() {
	alert("inside json");
	   var people = [];

	   $.getJSON('/static/json/priorities.json', function(data) {
	   			alert("inside json");
	       $.each(data.person, function(i, f) {
	          var tblRow = "<tr>" + "<td>" + f.firstName + "</td>" +
	           "<td>" + f.lastName + "</td>" + "<td>" + f.job + "</td>" + "<td>" + f.roll + "</td>" + "</tr>"
	           $(tblRow).appendTo("#userdata tbody");
	     });

	   });

	});
	
	

	
	        
	        $(document).ready(function(){
	        
	    	//$.cookie.raw = true;
	    	//alert("session " +$.cookie("sessionid",  { path: '/' }));
	    	//var ca = document.cookie;
	    	//alert("ses" + ca);
	        var socket = io.connect('http://100.98.13.53:8010');
	        socket.on('channel_console',
	            function (data) {
	                console.log(data);
	                // add comment to list
	    		var sessionid='{{session}}';
	            var obj = JSON.parse(data);
	            //alert("outside the print");
	            //alert("sessionid "+ sessionid);
	            //alert("obj.session_id "+ obj.session_id);
	            if(sessionid == obj.session_id)
	          	{
	            //alert("ll print now");
	    		        
	     var tblRow = "<tr>" + "<td>" + obj.submit_date + "</td>" +
	               "<td>" + obj.message + "</td>" + "</tr>"
	               $(tblRow).appendTo("#userdata tbody");
	            
	            //$('#consoleBox').append(obj.message+ " -- "+obj.session_id+"&#13;&#10;");
	            
	           //$('#consoleBox').append("<li>Hello</li>");
	            
	    		$('#consoleBox').scrollTop($('#consoleBox')[0].scrollHeight)
	           console.log("++++ "+obj.submit_date);
	            
	            }
	            });

	      

	        socket.on('channel_file_path',
	                function (data) {
	                    console.log(data);
	                    // add comment to list
	        		var sessionid= '{{session}}';
	                var obj = JSON.parse(data);
	                //alert("outside the print");
	                //alert("sessionid "+ sessionid);
	                //alert("obj.session_id "+ obj.session_id);
	                
	                if(sessionid == obj.session_id)
	              	{
	                //alert("ll print now");
	        		
	                filename = obj.message;
	            	alert(filename);
	                
	         		console.log(obj.message); 
	         		//document.getElementById("results1").innerHTML = "";
	         	      document.getElementById("demo").innerHTML = filename;
	         	      
	         	     var file_name=document.getElementById("demo").innerHTML;
	         	  	alert(file_name);
	         	      //document.getElementById("hideform").style.display="none";
	         	      //document.getElementById("results").style.display = "none";
	         	        //document.getElementById("b1").style.display = "none";
	         	         //document.getElementById("submit").style.display = "none";
	         	         alert("just before func1");
	         	     func1();
	         	     alert("just after func1");
	         	        function func1() {
	         	        	alert("hey inside func1");

	         	        	loadJSON(function(response) {
	         	        		alert("hey inside func2");
	         	        			// Parse JSON string into object
	         	        	  		var data1 = JSON.parse(response);     	        			
	         	        	  		alert(data1["BIOS"][0]["current_val"]);
	         	        			var results1= document.getElementById("results1");
	         	        			//var data = ["SERIAL","STATUS", "ATTRIBUTE", "CHECKBOX"]
	         	        			alert("1");
	         	        			var data = ["SERIAL","STATUS", "ATTRIBUTE"] 
	         	        		  	text = data1;
	         	        			alert("2");
	         	        			table = document.createElement('table');
	         	        			$(table).addClass("table table-striped table-bordered bootstrap-datatable datatable");
	         	        	    	thead = document.createElement('thead');
	         	        			tr = document.createElement('tr');
	         	        			
	         	        			for (var i = 0; i < data.length; i++) {
	         	        				var headerTxt = document.createTextNode(data[i]);
	         	        				$(headerTxt).addClass("center");
	         	        				th = document.createElement('th');
	         	        				th.appendChild(headerTxt);
	         	        				$(th).addClass("center");
	         	        				tr.appendChild(th);
	         	        				thead.appendChild(tr);
	         	        	  			  }
	         	        		
	         	        			table.appendChild(thead);
	         	        			for(i = 0; i < text.BIOS.length; i++) {
	         	        			tr = document.createElement('tr');
	         	        			td=document.createElement('td');
	         	        			$("td").addClass("center");
	         	        			tr.appendChild(td);
	         	        			td=document.createElement('td');
	         	        			tr.appendChild(td);
	         	        			td=document.createElement('td');
	         	        			tr.appendChild(td);
	         	        			//td=document.createElement('td');
	         	        	    	//$("td").addClass("center");
	         	        			//tr.appendChild(td); //Added for checkg box
	         	        	        //var checkbox = document.createElement("INPUT"); //Added for checkbox
	         	        	       //checkbox.type = "checkbox"; //Added for checkbox
	         	        			//checkbox.name = "abc"+i;
	         	        			//checkbox.id = "abc"+i;
	         	        			
	         	        			//checkbox.disabled="disabled";
	         	        			//checkbox.style="display:none";
	         	        			//$("checkbox").addClass("checkbx");
	         	        			tr.cells[0].appendChild(document.createTextNode(i+1));
	         	        			if(!(text.BIOS[i].current_val))
	         	        			
	         	        				tr.cells[1].appendChild(document.createTextNode("NA"));
	         	        			else
	         	        				tr.cells[1].appendChild(document.createTextNode(text.BIOS[i].current_val));
	         	        			
	         	        			//tr.cells[1].appendChild(document.createTextNode(text.BIOS[i].current_val));
	         	        	        tr.cells[2].appendChild(document.createTextNode(text.BIOS[i].attribute));
	         	        	      
	         	        	        //tr.cells[3].appendChild(checkbox); //Added for checkbox
	         	        			table.appendChild(tr);
	         	        	    }
	         	        			tablearea.appendChild(table);
	         	        			document.getElementById("table").style.display = "block"; 
	         	        			
	         	        			 });}

	         		//var path = "/static\/json";
	        		//var x = "/";
	        
	        		//alert(a);
	        		//var url=path + x+ filename;
	         		//$.getJSON(url,
	         			//	function(data){
	         				//var ttext = (data["SearchResponse"]["Translation"]["Results"][0]["TranslatedTerm"]);
	         				//alert("text" + ttext);
	         				//}
	         				//);
	         		
	         		
	         		
	                }
	                });
	        
	        
	        
	        
	        
	        
	        });
	  



			

		
		
