<html>
<head>
<title>{{title}}</title>
</head>
<body bgcolor='eeeeee'>

<!-- header image and title -->
% if username:
  % if not veteran:
    <div align="right"><p><a href="veteran">[ hide tutorial ]</a></p></div>
  % end
  % if veteran:
    <div align="right"><p><a href="green">[ show tutorial ]</a></p></div>
  % end
% end

<center>
<p><img src="image/mm_sol7_logo.png"></p>
<p><b>ASTECH</b>: easier MegaMek server administration. (ver. 0.4)<br />

% if username:
<font size="-1">You are logged as {{username}}.</font></p>

<!-- main menu -->
<p><a href="/">server status</a> | <a href="maps">map files</a> | <a href="saves">saved games</a> | <a href="units">units</a> | <a href="firststrike">help</a> | <a href="logout">log out</a></p>
% end
