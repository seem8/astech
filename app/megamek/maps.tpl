% include('header', title='Map files - Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    This is a MegaMek map upload form. Click <i>browse</i> to choose file
    with a .board extension on your computer, witch is typically in your
    data/boards folder. Choose one file at a time. I has to have .board
    extension (with is standard file from MegaMek map editor) and be below
    1 megabyte in size. File will be uploaded to data/boards/astech folder
    on your MegaMek server. You have to restart the server to play on new maps.
    <hr>
    Below that is the list of uploaded maps. You can choose them in the game options
    in MegaMek lobby screen. Remember to search them by size in MegaMek. You also
    can delete and download your uploaded maps with link in the left.
</div>
% end

<table>
  <tr width=500px>
    <td width=250px>
      <b>Upload map:</b>
      <p class="hint">Only files with .board extension are allowed.</p>
    </td>
    <td width=250px>
      % # map upload form
      <form action="/maps" method="post" enctype="multipart/form-data">
        <input type="file" name="map_file"><br>
        <input type="submit" value="Upload">
        % # wrongboard, bigboard and noboard are cookies set when
        % # the file doesn't met certain conditions
        <p class="error">
          % if wrongboard:
            Choose file with .board extension.
          % end
          % if bigboard:
            File is too big.
          % end
          % if noboard:
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
    <td width=720px>
      <strong>Here are your maps:</strong>
    </td>
  </tr>
  % # mapfiles is a list of all filenames from the maps directory
  % if len(mapfiles) > 0:
    % for map in mapfiles:
      <tr width=800px>
        <td width=40px><a href="/remove/map/{{map}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/download/map/{{map}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{map}}</td>
      </tr>
    % end
  </table>
  % end
  
  % if len(mapfiles) == 0:
    </table>
    <p>You have no custom maps yet.</p>
  % end

% # contact information and closing html tags
% include('footer')
