<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>{{title}}</title>
<meta name="author" content="Łukasz Posadowski">
<meta name="keywords" content="battletech, megamek">
<meta name="description" content="Play Battletech online easly. Web frontend for MegaMek server.">
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
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
<p><b>ASTECH</b>: easier MegaMek server administration. (ver. 0.1)<br />

% if username:
<font size="-1">You are logged as {{username}}.</font></p>

<!-- main menu -->
<p><a href="/">server status</a> | <a href="maps">map files</a> | <a href="saves">saved games</a> | <a href="units">units</a> | <a href="firststrike">help</a> | <a href="logout">log out</a></p>
% end
<p>&nbsp;</p>
