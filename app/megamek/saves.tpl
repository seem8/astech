% include('header', title='Saved games - Astech: easier  MegaMek administration')

% # tutorial messages in veteran cookie is absent
% if not veteran:
  <div id="tutorial">
    <strong>Tutorial:</strong><br>
    This is a MegaMek saves upload form. Click <em>browse</em> to choose
    file with a .sav.gz extension on your computer, witch is typically
    in your savegames folder. Choose one file at a time. I has to have .gz
    extension (with is standard file from MegaMek save game) and be below
    1 megabyte in size. File will be uploaded to savegames folder on your
    MegaMek server and a timestamp will be added to filename. You have to
    restart the server to load new save.
    <hr>
     Below that is the list of uploaded saves. You also can delete and
     download your uploaded saves with link in the left. To load a game
     type <em>/load [datestamp-filename]</em> in MegaMek lobby screen.
</div>
% end

<table>
  <tr width=500px>
    <td width=250px>
      <strong>Upload save:</strong>
      <p class="hint">Only files with .gz extension are accepted</p>
    </td>
    <td width=250px>
      % # saves upload form
      <form action="/saves" method="post" enctype="multipart/form-data">
        <input type="file" name="saved_game" /><br />
        <input type="submit" value="Upload" />
        % # wrongsave, bigsave and nosave are cookies set when
        % # file doesn't met certain conditions
        <p class="error">
          % if wrongsave:
            Choose file with .gz extension.
          % end
          % if bigsave:
            File is too big.
          % end
          % if nosave:
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
      <strong>Here are your saves:</strong>
    </td>
  </tr>
  % # savegames is a list with all filenames from the saves directory
  % if len(savegames) > 0:
    % for save in savegames:
      <tr width=800px>
        <td width=40px><a href="/remove/savegame/{{save}}"><img src="/image/delete.png"></a></td>
        <td width=40px><a href="/download/savegame/{{save}}"><img src="/image/download.png"></a></td>
        <td width=720px>{{save}}</td>
    </tr>
  % end
</table>
% end

% if len(savegames) == 0:
  </table>
  <p>You have no saved games yet.</p>
% end

% # contact information and closing html tags
% include('footer')
