import { useState } from "react"
import ButtonShowSongs from "./ButtonShowSongs"
import Collapse from 'react-bootstrap/Collapse'

const PlaylistRow = ({ playlist }) => {
  const [open, setOpen] = useState(false);
  
  return(
    <>
      <tr>
        <td className='column-1'>{playlist.title}</td>
        <td className='column-2'>{playlist.created_by ? playlist.created_by.username : "unknown"}</td>
        <td className='column-3 center-text'>{playlist.add_date.split('T')[0]}</td>
        <td className='column-4 center-text'>
        <ButtonShowSongs open={open} setOpen={setOpen}/>
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