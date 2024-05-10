import { useState } from "react"
import ButtonShowSongs from "./ButtonShowSongs"
import ButtonDeletePlaylist from "./ButtonDeletePlaylist"
import Collapse from 'react-bootstrap/Collapse'

const PlaylistRow = ({ playlist, setPlaylists }) => {
  const [open, setOpen] = useState(false);
  
  return(
    <>
      <tr>
        <td className='column-1 column-first'>{playlist.title}</td>
        <td className='column-2 column-mid'>{playlist.created_by ? playlist.created_by.username : "unknown"}</td>
        <td className='column-3 column-mid center-text'>{playlist.add_date.split('T')[0]}</td>
        <td className='column-4 column-last center-text'>
        <ButtonShowSongs open={open} setOpen={setOpen}/>
        <ButtonDeletePlaylist playlist={playlist} setPlaylists={setPlaylists}/>
        </td>
      </tr>
      <Collapse in={open}>
        <div className="collapse-song-list">
          {playlist.songs.map(song => (
            <tr>
              <td>
                {song.title}
              </td>
              <td>
                {song.artist}
              </td>
              <td>
                {song.url_field}
              </td>
            </tr>
          ))}
        </div>
      </Collapse>
    </>
  );
}

export default PlaylistRow;