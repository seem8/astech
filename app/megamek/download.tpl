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
      <font size="-1">Astech is now downloading MegaMek. Please do not refresh, or close this page. You will be redirected to Options page as soon as MegaMek will be installed.</font>
    </td>
  </tr>
</table>
% end

<p>Astech is downloading MegaMek {{release}}.</p>
<p>It may take a minute.</p>

% # contact information and closing html tags
% include('footer')
