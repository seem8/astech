% include('header', title='Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">This are Astech options. You can disable / enable tutorial and change Your MegaMek version. If You want to change name, or port of Your MegaMek server, contact me about it.</font>
    </td>
  </tr>
</table>
% end

<table>
  <tr width=200px>
    <td width=100px>
      &nbsp;<br><b>Tutorial:<br>&nbsp;</b>
    </tdi>
    <td width=100px>
    % if veteran:
      <a href="/green">enable</a>
    % end

    % if not veteran:
      <a href="/veteran">disable</a>
    % end
    </td>
  </tr>
</table>

<table>
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px><b>Here are your versions of MegaMek:</b></td>
  </tr>
  % # versions is a list of all filenames from the meks directory
  % if len(versions) > 0:
    % for ver in versions:
      <tr width=800px>
        <td width=40px><a href="/remove/map/{{ver}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/download/map/{{ver}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{ver}}</td>
      </tr>
    % end
  </table>
  % end
  
% if len(versions) == 0:
  </table>
  <p>You have no custom maps yet.</p>
% end

% # contact information and closing html tags
% include('footer')
