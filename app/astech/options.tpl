% include('header', title='Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    This are Astech options. You can show/hide tutoriall
    messages. If You want to change name, or port of Your
    MegaMek server, contact me about it.
    <hr>
    Below that you can change your megamek server version. Click
    an arrow in front of desired version. Choosen version has
    "check" icon in front of it.
  </div>
% end

<table>
  <tr width=200px>
    <td width=100px>
      <strong>Tutorial:</strong>
    </td>
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

<hr>

<table class="list">
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
  <p>You have no availble MegaMek version.</p>
% end


% # contact information and closing html tags
% include('footer')

