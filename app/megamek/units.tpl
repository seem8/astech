% include('header', title='Units - Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
      <strong>Tutorial:</strong><br>
      This is a MegaMek units upload form. Click <em>browse</em> to
      choose file with a .mtf extension on your computer. Choose one
      file at a time. I has to have .mtf extension (with is standard
      file from MegaMek Lab) and be below 1 megabyte in size. File will
      be uploaded to data/mechfiles/astech folder on your MegaMek server.
      You have to restart the server to use a new unit.
      <hr>
      Below is the list of uploaded custom units. You, as well as any other
      player, can choose them in the lobby screen. You also can delete and
      download your uploaded saves with link in the left.
  </div>
% end

<table border="0">
  <tr width=500px>
    <td width=250px>
      <b>Upload unit:</b>
      <p class="hint">Only files with .mtf extension are accepted.</p>
    </td>
    <td width=250px>
      % # unit upload form
      <form action="/units" method="post" enctype="multipart/form-data">
        <input type="file" name="unit_file"><br>
        <input type="submit" value="Upload">
      % # wrongunit, bigunit and nounit are cookies set when
      % # file doesn't met certain conditions
      <p class="error"> 
        % if wrongunit:
          Choose file with .mtf extension.
        % end
        % if bigunit:
          File is too big.
        % end
        % if nounit:
          Please choose a file first.
        % end
      </p>
    </td>
  </tr>
</table>

<hr>

<table class="list">
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px><b>Here are your custom units:</b></td>
  </tr>
  % if len(unitfiles) > 0:
    % for unit in unitfiles:
    % # unitfiles is a list with all filenames from the unit directory
      <tr width=800px>
        <td width=40px><a href="/remove/unit/{{unit}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/download/unit/{{unit}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{unit}}</td>
      </tr>
    % end
</table>
% end

% if len(unitfiles) == 0:
  </table>
  <p>You have no custom units yet.</p>

% # contact information and closing html tags
% include('footer')
