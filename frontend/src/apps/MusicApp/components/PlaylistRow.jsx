import { useState } from "react"
import ButtonShowSongs from "./ButtonShowSongs"
import ModalDeletePlaylist from "./ModalDeletePlaylist"
import Collapse from 'react-bootstrap/Collapse'
import Table from 'react-bootstrap/Table'
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
        <ModalDeletePlaylist playlist={playlist} setPlaylists={setPlaylists}/>
        </td>
      </tr>
      <tr>
        <td colSpan="4" className="subtable-row">
          <Collapse in={open}>
            <div className="playlist-row collapse-song-list" data-playlist-id={playlist.id}>
              <Table hover className="song-subtable">
                <tbody>
                  {playlist.songs.map((song) => (
                    <tr key={`${playlist.id}-${song.id}`}>
                      <td className="column-song-title">{song.title}</td>
                      <td className="column-song-artist">{song.artist}</td>
                      <td className="column-song-url">{song.url_field}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          </Collapse>
        </td>
      </tr>
    </>
  );
}

export default PlaylistRow;