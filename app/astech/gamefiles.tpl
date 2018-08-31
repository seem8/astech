% include('header', title='Map files - Astech: easier MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    This is a MegaMek files upload form. Click <i>browse</i> to choose file
    with a .board, .sav.gz, or .mtf extension on your computer, witch is typically
    in your data, or savegames folder. Choose one file at a time. I has to have
    appropriate extension, file size below 1.5 megabytes and name below 80 characters.
    <hr>
    Below that is the list of uploaded files. You can choose them in the game options
    in MegaMek lobby screen. You also can delete and download your uploaded maps
    with images in the left.
</div>
% end

<table>
  <tr width=500px>
    <td width=250px>
      <b>Upload file:</b>
      <p class="hint">Only files with .board, .mtf, or save.gz<br>
                      extension are allowed.</p>
    </td>
    <td width=250px>
      % # map upload form
      <form action="/gamefiles" method="post" enctype="multipart/form-data">
        <input type="file" name="posted_file"><br>
        <input type="submit" value="Upload">
        <p class="error">
          % if wrongfile:
            Choose file with .board, .mtf, or .sav.gz extension.
          % end
          % if bigfile:
            File is too big.
          % end
          % if nofile:
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
  % if len(map_list) > 0:
    % for map in map_list:
      <tr width=800px>
        <td width=40px><a href="/files/remove/map/{{map}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/files/download/map/{{map}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{map}}</td>
      </tr>
    % end
  </table>
  % end
  
  % if len(map_list) == 0:
    </table>
    <p>You have no custom maps yet.</p>
  % end

<hr>

<table class="list">
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px>
      <strong>Here are your units:</strong>
    </td>
  </tr>
  % # unitfiles is a list of all filenames from the units directory
  % if len(unit_list) > 0:
    % for unit in unit_list:
      <tr width=800px>
        <td width=40px><a href="/files/remove/unit/{{unit}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/files/download/unit/{{unit}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{unit}}</td>
      </tr>
    % end
  </table>
  % end
  
  % if len(unit_list) == 0:
    </table>
    <p>You have no custom units yet.</p>
  % end

<hr>

<table class="list">
  <tr width=800px>
    <td width=40px></td>
    <td width=40px></td>
    <td width=720px>
      <strong>Here are your saves games:</strong>
    </td>
  </tr>
  % # saves is a list of all saved games from the savedgames directory
  % if len(save_list) > 0:
    % for save in save_list:
      <tr width=800px>
        <td width=40px><a href="/files/remove/savegames/{{save}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/files/download/savegames/{{save}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{save}}</td>
      </tr>
    % end
  </table>
  % end
  
  % if len(save_list) == 0:
    </table>
    <p>You have no custom maps yet.</p>
  % end

% # contact information and closing html tags
% include('footer')

