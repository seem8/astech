% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">This is a MegaMek units upload form. Click BLE to choose file with a .mtf extension on your computer. Choose one file at a time. I has to have .mtf extension (with is standard file from MegaMek Lab) and be below 1 megabyte in size. File will be uploaded to data/mechfiles/astech folder on your MegaMek server. You have to restart the server to use a new unit.</font>
    </td>
  </tr>
</table>
% end

<table border="0">
  <tr width=500px>
    <td width=250px valign="TOP">
      <b>Upload unit:</b><br /><font size="-1">Only files with .mech extension are accepted.</font></td>
    <td width=250px valign="TOP">
      <form action="/maps" method="post" enctype="multipart/form-data">
        <input type="file" name="unit_file" /><br />
        <input type="submit" value="Upload" />
    </td>
  </tr>
</table>
<p>&nbsp;</p>

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=800px>
    <td width=800px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=800px>
    <td width=800px>
      <font size="-1">Below is the list of uploaded custom units. You, as well as any other player, can choose them in the lobby screen.<br />You also can delete your uploaded units with <i>delete</i> link in front of each of them.</font>
    </td>
  </tr>
</table>
% end

<table>
  <tr width=800px>
    <td width=60px></td>
    <td width=740px><b>Here are your units:</b></td>
  </tr>
  % for unit in unitfiles:
    <tr width=800px>
      <td width=80px>ble</td>
      <td width=740px>{{unit}}</td>
    </tr>
  % end
</table>

% include('footer')
