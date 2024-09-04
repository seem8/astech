% include('header', title='Astech: easier MegaMek administration')

<form action="/login" method="post">
<table border="0">
  <tr width=300px>
    <td width=150px>Username:</td>
    <td width=150px><input name="username" type="text"></td>
  </tr>
  <tr width=300px>
    <td width=150px>Password:</td>
    <td width=150px><input name="password" type="password"></td>
  </tr>
  <tr width=300px>
    <td width=150px>&nbsp;</td>
    <td width=150px><input value="Login" type="submit"></td>
  </tr>
</table>
</form>

% # badpass is a cookie set when wrong login and/or password were submitted
% if badPassword:
  <p class="error">Wrong login, or password.</p>
% end

<p><em>Astech page is using cookies to work properly.</em><br>
<em>We do not track You. We just want to know if You're logged in.</p>

% # contact information and closing html tags
% include('footer')
