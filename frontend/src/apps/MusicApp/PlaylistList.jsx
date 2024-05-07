import { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table'
import PlaylistRow from './PlaylistRow'
import axios from 'axios';

const PlaylistList = () => {
  // make axios call to get playlists with useEffect
  const [playlists, setPlaylists] = useState([]);
  useEffect(() => {
    axios.get('http://localhost:8000/music/playlists/')
      .then((response) => {
        setPlaylists(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data: ', error);
      });
  }
  , []);
  
  return (
    <div className="playlist-table">
      <Table bordered hover>
        <thead>
          <tr>
            <th className='column-1'>Playlist Name</th>
            <th className='column-2'>Created By</th>
            <th className='column-3 center-text'>Created Date</th>
            <th className='column-4 center-text'></th>
          </tr>
        </thead>
        <tbody>
          {playlists.map((playlist) => (
            <PlaylistRow playlist={playlist}/>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default PlaylistList;