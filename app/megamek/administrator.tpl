% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=750px>
    <td width=250px>
      <b><font size="-1">Tutorial:</font></b>
    </td>
    <td width=250px></td>
    <td width=250px></td>
  <tr>
  <tr width=750px>
    <td width=250px valign="TOP">
      <font size="-1">Basic server information:<br />
      - version of MegaMek,<br />
      - address of Astech server,<br />
      - port number for MegaMek server.</font>
    </td>
    <td width=250px valign="TOP">
      <font size="-1">Optional password for changing game options. Use this if you don't know, or trust, your players. Astech accepts only latin characters (A-Z, a-z) at the moment.</font>
    </td>
    <td width=250px valign="TOP">
      <font size="-1">Here you can turn on/off your MegaMek server.</font>
    </td>
  </tr>
</table>
% end
      
<table>
  <tr width=750px>
    <td width=250px><b>Server info</b></td>
    <td width=250px><b>Game password</b></td>
    <td width=250px><b>Master switch</b></td>
  <tr width=750opx>
    <td width=250px valign="TOP">
        version: {{mtver}}<br />
        address: {{mtdomain}}<br />
        port: {{mtport}}
      </td>
      <td width=250px valign="TOP">
        <form action="/" method="post">
          % if mtpassword:
            <input name="mekpassword" type="text" value="{{mtpassword}}" /><br />
          % end
          % if not mtpassword:
            <input name="mekpassword" type="text" /><br />
          % end
          <font size="-1">(please use only latin characters)</font></br />
          <input value="Set" type="submit" />
        </form>
      <td width=250px valign="TOP">
        % if not mtison:
          <a href="mmturnon"><img src="image/server_off.png"></a>
        % end
        % if mtison:
          <a href="mmturnoff"><img src="image/server_on.png"></a>
        % end
      </td>
    </tr>
</table>

<p>&nbsp;</p>

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=700px>
    <td width=700px>
      <font size="-1"><b>Tutorial:</b>
    </td>
  </tr>
  <tr width=700px>
    <td width=700px>
      <font size="-1">Below is 40 newest lines of megameklog.txt file. It's not game log file that you see on MegaMek window below the map, nor a savegame info. It provides output of players joining and leaving MegaMek server, as well some additional information for troubleshooting (eg. wrong MegaMek versions). Astech will not autorefresh this file, so to see exact newest logs, refresh server status page.</font>
    </td>
  </tr>
</table>
% end

<table>
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

% include('footer')
