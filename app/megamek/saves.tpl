% include('header', title='Astech - for better MegaMek administration')

% if tutorial:
  <table>
    <tr width=800px>
      <td>
        <p>This is a <b>saves</b> page, where you can upload them to<br />
           Astech webpage and use them when launching MegaMek.</p>
        <p>Savegame files are usually in your <i>savegames</i> on your<br />
           local MegaMek installation folder and have .sav.gz extension.<br />
           After uploading, they will be at megamek/savegames on<br />
           this server.</p>
        <p>You can try it now, or <a href="administrator">continue tutorial</a>.</p>
      </td>
    </tr>
  </table>
% end

<p>
<table border="0">
  <tr width=500px>
    <td width=250px>
      <b>Upload save:</b><br /><font size="-1">Only files with .gz extension are accepted.</font></td>
    <td width=250px>
      <form action="/saves" method="post" enctype="multipart/form-data">
        <input type="file" name="saved_game" /><br />
        <input type="submit" value="Upload" />
    </td>
  </tr>
</table>
</p>

<p>
<table border="1">
  <tr width=800px>
    <td width=60px></td>
    <td width=740px>Here are your saves:</td>
  </tr>
  % for save in savegames:
    <tr width=800px>
      <td width=80px>ble</td>
      <td width=740px>{{save}}</td>
    </tr>
  % end
</table>
<p>

% include('footer')
