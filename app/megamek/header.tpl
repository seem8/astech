<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>{{title}}</title>
<meta name="author" content="Łukasz Posadowski">
<meta name="keywords" content="battletech, megamek, astech">
<meta name="description" content="Play Battletech online easly. Web frontend for MegaMek server.">
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body bgcolor='eeeeee'>

<!-- header image and title -->
<center>
<p><img src="/image/astech_logo.png"></p>
<p><b>ASTECH</b>: easier MegaMek server administration. (ver. 0.2)<br />

% if username:
<font size="-1">You are logged as {{username}}.</font></p>

<!-- main menu -->
% if username:
  % if not veteran:
    <p><a href="/">server status</a> | <a href="/maps">map files</a> | <a href="/saves">saved games</a> | <a href="/units">units</a> | <a href="/veteran">hide tutorial</a> | <a href="/logout">log out</a><br />&nbsp;</p>
  % end
% if veteran:
    <p><a href="/">server status</a> | <a href="maps">map files</a> | <a href="saves">saved games</a> | <a href="units">units</a> | <a href="green">show tutorial</a> | <a href="logout">log out</a><br />&nbsp;</p>
  % end
% end
