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
