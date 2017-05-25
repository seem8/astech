% include('header', title='Astech - for better MegaMek administration')

% if not veteran:
  <table>
    <tr width=800px>
      <td width=800px>
        <p>This is a <b>Units page</b> page, where you can upload them to Astech webpage and choose them in MegaMek lobby screen.</p>
        <p>Keep it simple. Please avoid file names with spaces, or special characters.</p>
        <p>Unit files are usually in <i>data/mechfiles</i> on your local MegaMek installation folder and have .board extension.<br />
           After uploading, they will be at <i>data/mechfiles/astech on this server</i>.</p>
      </td>
    </tr>
  </table>
% end

<table border="0">
  <tr width=500px>
    <td width=250px>
      <b>Upload unit:</b><br /><font size="-1">Only files with .mech extension are accepted.</font></td>
    <td width=250px>
      <form action="/maps" method="post" enctype="multipart/form-data">
        <input type="file" name="unit_file" /><br />
        <input type="submit" value="Upload" />
    </td>
  </tr>
</table>
<p>&nbsp;</p>

<table>
  <tr width=800px>
    <td width=60px></td>
    <td width=740px>Here are your units:</td>
  </tr>
  % for unit in unitfiles:
    <tr width=800px>
      <td width=80px>ble</td>
      <td width=740px>{{unit}}</td>
    </tr>
  % end
</table>

% include('footer')
