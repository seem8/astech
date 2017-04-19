% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
<p>
  <table>
    <tr width=800px>
      <td width=800px>
        <p>This is a <b>server status</b> page, where you can control MegaMek server and view log files.</p>
        <p>In server status table you can start, stop or quick restart MegaMek instance.<br />
           MegaMek server will listen on specified port on entire intrernet.<br />
           Remember that players (including yourself) have to have the same version of MegaMek to connect.</p>
        <p>MegaMek Server Log table is showing you the lastest messages from Megamek installed on Astech webpage. It will show players connecting and disconnecting, their MegaMek version and all possible problems with joining game. It will not autorefresh, so hit F5 from time to time to refresh entire webpage.</p>
      </td>
    </tr>
<p>
% end 

<table border="1">
  <tr width=500px>
    <td width=250px>Server status:</td>
    <td width=250px>
      % if mmison:
        server is <b>turned on</b>
      % end
      % if not mmison:
        server is <b>turned off</b>
      % end
      <br />
      version: {{mmver}}<br />
      address: {{domain}}<br />
      port: {{port}}
    </td>
  </tr>
  <tr width=500px>
    <td width=250px>Server administration:</td>
    <td width=250px>
      % if not mmison:
        <a href="mmturnon">turn on</a>
      % end
      % if mmison:
        <a href="mmturnoff">turn off</a>
      % end
      <br /><a href="mmrestart">quick restart</a>
      <br /><font size = '-1'>If you turn off, or restart the server,<br />
      game in progress will be lost.</font>
    </td>
  </tr>
</table>
</p>


% if mmison:
<p>&nbsp;</p>
<p>
<table border="0">
  <tr width=476px>
    <td width=175px>&nbsp;</td>
    <td width=292px>How to connect to the game:</td>
  </tr>
  <tr width=467px>
    <td width=175px><img src="/image/connect_dialog-0-0.png"></td>
    <td width=292px><img src="/image/connect_dialog-1-0.png"></td>
  </tr>
  <tr width=467px>
    <td width=175px><img src="/image/connect_dialog-0-1.png"></td>
    <td width=292px><img src="/image/connect_dialog-1-1.png"></td>
  </tr>
  <tr width=467px>
    <td width=175px><img src="/image/connect_dialog-0-2.png"></td>
    <td width=292px><img src="/image/connect_dialog-1-2.png"></td>
  </tr>
  <tr width=467px>
    <td width=175px><img src="/image/connect_dialog-0-3.png"></td>
    <td width=292px><img src="/image/connect_dialog-1-3.png"></td>
  </tr>
  <tr width=467px>
    <td width=175px><img src="/image/connect_dialog-0-4.png"></td>
    <td width=292px><img src="/image/connect_dialog-1-4.png"></td>
  </tr>
</table>
</p>
% end

<p>&nbsp;</p>

<p>
<table border=0>
  <tr>
    <td width=700px>
      <p><b>Megamek server log</b> (newest first):</p>
    <td>
  </tr>
  % for i in getLogFile:
    <tr>
      <td width=700px>{{i}}</td>
    </tr>
  % end
  <tr><td width=700px>[...]</td></tr>
</table>
<p>

% include('footer')
