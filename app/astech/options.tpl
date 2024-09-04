% include('header', title='Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    You can show/hide tutorial messages.
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

% # contact information and closing html tags
% include('footer')

