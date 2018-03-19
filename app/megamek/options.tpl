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
      &nbsp;<br><b>Tutorial:</b><br>&nbsp;
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

% # tutorial messages in veteran cookie is absent
% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">Here you can change your megamek server version. Press arrow in front of desired version. Choosen version has "check" icon in front of it.</font>
    </td>
  </tr>
</table>
% end
<table>
  <tr width=600px>
    <td width=40px></td>
    <td width=460px><b>Here are your versions of MegaMek:</b></td>
  </tr>
  % # versions is a list of all filenames from the meks directory
  % if len(versions) > 0:
    % for ver in versions:
      <tr width=600px>
        <td width=40px>
        % if ver == selected:
          <img src="/image/selected.png"></a>
        % end
        % if ver != selected:
          <a href="/ver/{{ver}}"><img src="/image/select.png"></a>
        % end
        </td>
        <td width=460px>Megamek {{ver}}</td>
      </tr>
    % end
</table>
% end
  
% if len(versions) == 0:
  </tr></table>
  <p>You have no custom maps yet.</p>
% end

% # contact information and closing html tags
% include('footer')
