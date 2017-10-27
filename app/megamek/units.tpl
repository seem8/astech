% include('header', title='Units - Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">This is a MegaMek units upload form. Click <i>browse</i> to choose file with a .mtf extension on your computer. Choose one file at a time. I has to have .mtf extension (with is standard file from MegaMek Lab) and be below 1 megabyte in size. File will be uploaded to data/mechfiles/astech folder on your MegaMek server. You have to restart the server to use a new unit.</font>
    </td>
  </tr>
</table>
% end

<table border="0">
  <tr width=500px>
    <td width=250px valign="TOP">
      <b>Upload unit:</b><br /><font size="-1">Only files with .mtf extension are accepted.</font></td>
    <td width=250px valign="TOP">
      % # unit upload form
      <form action="/units" method="post" enctype="multipart/form-data">
        <input type="file" name="unit_file" /><br />
      <input type="submit" value="Upload" />
      % # wrongunit, bigunit and nounit are cookies set when
      % # file doesn't met certain conditions
      % if wrongunit:
        <br /><font size="-1" color="red">Choose file with .mtf extension.</font>
      % end
      % if bigunit:
        <br /><font size="-1" color="red">File is too big.</font>
      % end
      % if nounit:
        <br /><font size="-1" color="red">Please choose a file first.</font>
      % end
    </td>
  </tr>
</table>
<p>&nbsp;</p>

% # tutorial messages in veteran cookie is absent
% if not veteran:
<table bgcolor='dddddd'>
  <tr width=800px>
    <td width=800px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=800px>
    <td width=800px>
      <font size="-1">Below is the list of uploaded custom units. You, as well as any other player, can choose them in the lobby screen.<br />You also can delete and download your uploaded saves with link in the left.</font>
    </td>
  </tr>
</table>
% end

<table>
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px><b>Here are your custom units:</b></td>
  </tr>
  % for unit in unitfiles:
  % # unitfiles is a list with all filenames from the unit directory
    <tr width=800px>
      <td width=40px><a href="remove/unit/{{unit}}"><img src="image/delete.png"></a></td>
      <td width=40px><a href="download/unit/{{unit}}"><img src="image/download.png"></a></td>
      <td width=720px>{{unit}}</td>
    </tr>
  % end
</table>

% # contant information and closing html tags
% include('footer')
