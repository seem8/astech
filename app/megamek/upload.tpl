% include('header', title='Astech - for better MegaMek administration')

<p>You are logged as {{username}}.</p>
<p>
<table border="1">
  <tr width=500px>
    <td width=250px>Upload save:</td>
    <td width=250px>
      <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="saved_game" /><br />
        <input type="submit" value="Upload" />
      </form>
    </td>
  <tr>
</table>
<p>

