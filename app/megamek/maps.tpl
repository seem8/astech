% include('header', title='Astech - for better MegaMek administration')

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
