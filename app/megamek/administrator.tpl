% include('header', title='Astech - for better MegaMek administration')

<p>
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
