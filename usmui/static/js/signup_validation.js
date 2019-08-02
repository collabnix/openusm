function pwd_match()
	{
		var pwd1=document.getElementById("p1");
		var pwd2=document.getElementById("p2");\
		
		
			if(pwd1.value==pwd2.value)
				return true;
			else
				{
					alert("password does not mattch");
					return p1.focus();
				}
	
			
	}
			