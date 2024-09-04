<!DOCTYPE html>
<html>
<head>
  <title>{{title}}</title>
  <meta name="author" content="SeeM">
  <meta name="keywords" content="battletech, megamek, astech">
  <meta name="description" content="Play Battletech online easly. Web frontend for MegaMek server.">
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/style" type="text/css">
</head>
<body>

% # header image and title
<div id="header">
  <img src="/image/astech_logo.png">

  <h1>ASTECH: easier MegaMek server administration. (ver. 0.7)</h1>

  % # username is a cookie with login
  % if username:
    <p class="login">You are logged as {{username}}.</font></p>
  % end
  % # warning about debug mode
  % if AST_DEBUG:
    <p class="hint">Astech is runinng in debug mode.</font></p>
  % end
</div>

% # main menu
% if username:
  <div class="nav">
    <p class="menu">
    <a href="/">server status</a> | 
    <a href="/gamefiles">game files</a> | 
    <a href="/options">options</a> | 
    <a href="/logout">log out</a>
  </div>
% end

