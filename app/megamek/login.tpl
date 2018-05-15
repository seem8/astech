% include('header', title='Astech: easier MegaMek administration')

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

% # comment those two lines on production
<p>Default login: <i>somelogin</i>,
default password: <i>somepassword</i></p>

% # badpass is a cookie set when wrong login and/or password were submitted
% if badPass:
  <p><font size = '-1' color="red">Wrong login, or password.</font></p>
% end

% # contant information and closing html tags
% include('footer')
