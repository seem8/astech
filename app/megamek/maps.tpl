% include('header', title='Map files - Astech: easier MegaMek administration')

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">This is a MegaMek map upload form. Click <i>browse</i> to choose file with a .board extension on your computer, witch is typically in your data/boards folder. Choose one file at a time. I has to have .board extension (with is standard file from MegaMek map editor) and be below 1 megabyte in size. File will be uploaded to data/boards/astech folder on your MegaMek server. You have to restart the server to play on new maps.</font>
    </td>
  </tr>
</table>
% end

<table border="0">
  <tr width=500px>
    <td width=250px valign="TOP">
      <b>Upload map:</b><br /><font size="-1">Only files with .board extension are allowed.</font></td>
    <td width=250px valign="TOP">
      <form action="/maps" method="post" enctype="multipart/form-data">
        <input type="file" name="map_file" /><br />
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
      <font size="-1">Below is the list of uploaded maps. You can choose them in the game options in MegaMek lobby screen. Remember to search them by size in MegaMek.<br />You also can delete and download your uploaded maps with link in the left.</font>
    </td>
  </tr>
</table>
% end

<table>
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px><b>Here are your maps:</b></td>
  </tr>
  % for map in mapfiles:
    <tr width=800px>
      <td width=40px><a href="remove/map/{{map}}"><img src="image/delete.png"></a></td>
      <td width=40px><a href="download/map/{{map}}"><img src="image/download.png"></a></td>
      <td width=720px>{{map}}</td>
    </tr>
  % end
</table>

% include('footer')
