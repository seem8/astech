% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
<table bgcolor='dddddd'>
  <tr width=500px>
    <td width=500px>
      <font size="-1"><b>Tutorial:</b></font>
    </td>
  <tr width=500px>
    <td width=500px>
      <font size="-1">This is a MegaMek saves upload form. Click <i>browse</i> to choose file with a .sav.gz extension on your computer, witch is typically in your savegames folder. Choose one file at a time. I has to have .gz extension (with is standard file from MegaMek save game) and be below 1 megabyte in size. File will be uploaded to savegames folder on your MegaMek server and a timestamp will be added to filename. You have to restart the server to load new save.</font>
    </td>
  </tr>
</table>
% end

<table border="0">
  <tr width=500px>
    <td width=250px valign="TOP">
      <b>Upload save:</b><br /><font size="-1">Only files with .gz extension are accepted.</font></td>
    <td width=250px valign="TOP">
      <form action="/saves" method="post" enctype="multipart/form-data">
        <input type="file" name="saved_game" /><br />
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
      <font size="-1">Below is the list of uploaded saves. You also can delete and download your uploaded saves with link in the left.<br />To load a game type <i>/load [file_name-datestamp]</i> in MegaMek lobby screen.</font>
    </td>
  </tr>
</table>
% end

<table>
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px><b>Here are your saves:</b></td>
  </tr>
  % for save in savegames:
    <tr width=800px>
      <td width=40px><a href="delsavegame/{{save}}"><img src="image/delete.png"></a></td>
      <td width=40px><a href="savegame/{{save}}"><img src="image/download.png"></a></td>
      <td width=720px>{{save}}</td>
    </tr>
  % end
</table>

% include('footer')
