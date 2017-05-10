% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
  <table>
    <tr width=800px>
      <td width=800px>
        <p>This is a <b>map files</b> page, where you can upload them to Astech webpage and choose them in MegaMek lobby screen.</p>
        <p>Keep it simple. Please avoid file names with spaces, or special characters.</p>
        <p>Map files are usually in <i>data/boards</i> on your local MegaMek installation folder and have .board extension.<br />
           After uploading, they will be at <i>data/boards/astech on this server</i>.</p>
      </td>
    </tr>
  </table>
% end

<p>
<table border="0">
  <tr width=500px>
    <td width=250px>
      <b>Upload map:</b><br /><font size="-1">Only files with .board extension are accepted.</font></td>
    <td width=250px>
      <form action="/maps" method="post" enctype="multipart/form-data">
        <input type="file" name="map_file" /><br />
        <input type="submit" value="Upload" />
    </td>
  </tr>
</table>
</p>

<p>
<table border="1">
  <tr width=800px>
    <td width=60px></td>
    <td width=740px>Here are your maps:</td>
  </tr>
  % for map in mapfiles:
    <tr width=800px>
      <td width=80px>ble</td>
      <td width=740px>{{map}}</td>
    </tr>
  % end
</table>
<p>

% include('footer')
