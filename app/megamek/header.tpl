<html>
<head>
<title>{{title}}</title>
</head>
<body bgcolor='eeeeee'>
<center>

<!-- header image and title -->
<p><img src="image/mm_sol7_logo.png"></p>
<p><b>ASTECH</b>: easier MegaMek server administration. (ver. 0.4)<br />
% if username:
<font size="-1">You are logged as {{username}}.</font></p>
% end

<!-- main menu -->
% if username:
<p><a href="/">server status</a> | <a href="saves">saved games</a> | <a href="maps">map files</a> | <a href="logout">log out</a></p>
% end
