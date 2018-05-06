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

% # header image and title
<center>
<p><img src="/image/astech_logo.png"></p>
<p><b>ASTECH</b>: easier MegaMek server administration. (ver. 0.4)<br />

% # username is a cookie with login
% if username:
<font size="-1">You are logged as {{username}}.</font></p>
% end

% # main menu
% if username:
<p><a href="/">server status</a> | <a href="/maps">map files</a> | <a href="/saves">saved games</a> | <a href="/units">units</a> | <a href="/options">options</a> | <a href="/logout">log out</a><br />&nbsp;</p>
% end
