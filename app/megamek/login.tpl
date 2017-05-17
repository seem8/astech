% include('header', title='Astech - for better MegaMek administration')

% if badPass:
  <p><font size = '-1'>Wrong login/password, try again.</font></p>
% end

<p>
<form action="/login" method="post">
<table border="0">
  <tr width=300px>
    <td width=150px>Username:</td>
    <td width=150px><input name="username" type="text" /></td>
  </tr>
  <tr width=300px>
    <td width=150px>Password:</td>
    <td width=150px><input name="password" type="password" /></td>
  </tr>
  <tr width=300px>
    <td width=150px>&nbsp;</td>
    <td width=150px><input value="Login" type="submit" /></td>
  </tr>
</table>
</form>
</p>

% include('footer')
