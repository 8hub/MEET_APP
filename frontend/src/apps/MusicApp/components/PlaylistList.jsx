import { useEffect } from 'react';
import Table from 'react-bootstrap/Table'
import PlaylistRow from './PlaylistRow'
import axios from 'axios';

const PlaylistList = ({playlists, setPlaylists}) => {
  // make axios call to get playlists with useEffect
  useEffect(() => {
    axios.get('http://localhost:8000/music/playlists/')
      .then((response) => {
        setPlaylists(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data: ', error);
      });
  }
  , [setPlaylists]);
  
  return (
    <div className="playlist-table">
      <Table bordered hover>
        <thead>
          <tr>
            <th className='column-1 column-first'>Playlist Name</th>
            <th className='column-2 column-mid'>Created By</th>
            <th className='column-3 column-last center-text'>Created Date</th>
            <th className='column-4 column-blank center-text' id='column-empty'></th>
          </tr>
        </thead>
        <tbody>
          {playlists.map((playlist) => (
            <PlaylistRow key={playlist.id} playlist={playlist} setPlaylists={setPlaylists}/>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default PlaylistList;