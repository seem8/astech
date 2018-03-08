% include('header', title='Server status - Astech: easier Megamek administration')

% # tutorial messages
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
      <font size="-1">Optional password for changing game options. Astech accepts only latin characters (A-Z, a-z) at the moment. To remove a password, set an empty one. You have to restart the server after changing password.</font>
    </td>
    <td width=250px valign="TOP">
      <font size="-1">Here you can turn on/off your MegaMek server. If MegaMek will clash, Astech will display OFF button.</font>
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
        % # variables from MegaTech class
        name: {{mtname}}<br />
        version: {{mtver}}<br />
        address: {{mtdomain}}<br />
        port: {{mtport}}
      </td>
      <td width=250px valign="TOP">
        % # setting password for changing game options
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
        % if noalpha:
          % # noalpha is a cookie set after trying to use nonlatin characters as a password
          <br /><font size="-1" color="red">Please use only latin characters as password.</font>
        % end
      </td>
      <td width=250px valign="TOP">
        % if not mtison:
          <a href="/mmturnon"><img src="/image/server_off.png"></a>
        % end
        % if mtison:
          <a href="/mmturnoff"><img src="/image/server_on.png"></a>
        % end
      </td>
    </tr>
</table>

<p>&nbsp;</p>

% # more tutorial messages
% if not veteran:
<table bgcolor='dddddd'>
  <tr width=700px>
    <td width=700px>
      <font size="-1"><b>Tutorial:</b>
    </td>
  </tr>
  <tr width=700px>
    <td width=700px>
      <font size="-1">Below is the megameklog.txt file. It's not game log file that you see on MegaMek window below the map, nor a savegame info. It provides output of players joining and leaving MegaMek server, as well as some additional information for troubleshooting (eg. wrong MegaMek versions). Astech will not autorefresh this file, so to see exact newest logs, refresh server status page.</font>
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
  % # megameklog.txt file in reverser order
  % for i in getLogFile:
    <tr>
      <td width=700px>{{i}}</td>
    </tr>
  % end
  <tr><td width=700px>[...]</td></tr>
</table>

% include('footer')
