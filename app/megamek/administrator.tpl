% include('header', title='Server status - Astech: easier Megamek administration')

% # tutorial messages
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    Here you have basic server information:
    <ul>
      <li>version of MegaMek,</li>
      <li>address of Astech server,</li>
      <li>port number for MegaMek server.</li>
    </ul>
    You may provide password for changing game options.
    Astech accepts only latin characters (A-Z, a-z).
    To remove a password, set an empty one.
    You have to restart the server after changing password.<br>
    Lastly, you can turn on/off your MegaMek server.
    If MegaMek will crash, Astech will display OFF button.
    <hr>
    Below that is the megameklog.txt file. It's not game log file
    that you see on MegaMek window below the map, nor a savegame info.
    It provides output of players joining and leaving MegaMek server,
    as well as some additional information for troubleshooting
    (eg. wrong MegaMek versions). Astech will not autorefresh this file,
    so to see exact newest logs, refresh server status page.
  </div>
% end
      
<table>
  <tr width=750px>
    <th width=250px>Server info</th>
    <th width=250px>Game password</th>
    <th width=250px>Master switch</th>
  <tr width=750px>
    <td width=250px>
        % # variables from MegaTech class
        name: {{mtname}}<br>
        version: {{mtver}}<br>
        address: {{mtdomain}}<br>
        port: {{mtport}}
      </td>
      <td width=250px>
        % # setting password for changing game options
        <form action="/" method="post">
          % if mtpassword:
            <input name="mekpassword" type="text" value="{{mtpassword}}" /><br>
          % end
          % if not mtpassword:
            <input name="mekpassword" type="text" /><br>
          % end
          <p class="hint">(please use only latin characters)</p>
          <input value="Set" type="submit">
        </form>
        % if noalpha:
          % # noalpha is a cookie set after trying to use nonlatin characters as a password
          <p class="hint">Please use only latin characters as password.</font>
        % end
      </td>
      <td width=250px>
        % if not mtison:
          <a href="/mmturnon"><img src="/image/server_off.png"></a>
        % end
        % if mtison:
          <a href="/mmturnoff"><img src="/image/server_on.png"></a>
        % end
      </td>
    </tr>
</table>

<hr>

<table class="list">
  <tr>
    <td>
      <h2>Megamek server log (newest first):</h2>
    <td>
  </tr>
  % # megameklog.txt file in reverser order
  % for i in logFile:
    <tr>
      <td>{{i}}</td>
    </tr>
  % end
  <tr>
    <td>[...]</td>
  </tr>
</table>

% include('footer')

