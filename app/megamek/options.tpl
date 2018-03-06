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

% if veteran:
<p><a href="/green">enable tutorial</a></p>
% end

% if not veteran:
<p><a href="/veteran">disable tutorial</a></p>
% end

% # contact information and closing html tags
% include('footer')
