% include('header', title='Saved games - Astech: easier  MegaMek administration')

% # tutorial messages in veteran cookie is absent
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
      % # saves upload form
      <form action="/saves" method="post" enctype="multipart/form-data">
        <input type="file" name="saved_game" /><br />
        <input type="submit" value="Upload" />
        % # wrongsave, bigsave and nosave are cookies set when
        % # file doesn't met certain conditions
        % if wrongsave:
          <br /><font size="-1" color="red">Choose file with .gz extension.</font>
        % end
        % if bigsave:
          <br /><font size="-1" color="red">File is too big.</font>
        % end
        % if nosave:
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
      <font size="-1">Below is the list of uploaded saves. You also can delete and download your uploaded saves with link in the left.<br />To load a game type <i>/load [datestamp-filename]</i> in MegaMek lobby screen.</font>
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
  % # savegames is a list with all filenames from the saves directory
  % for save in savegames:
    <tr width=800px>
      <td width=40px><a href="/remove/savegame/{{save}}"><img src="/image/delete.png"></a></td>
      <td width=40px><a href="/download/savegame/{{save}}"><img src="/image/download.png"></a></td>
      <td width=720px>{{save}}</td>
    </tr>
  % end
</table>

% # contant information and closing html tags
% include('footer')
