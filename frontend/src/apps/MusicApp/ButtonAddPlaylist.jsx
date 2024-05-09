import Button from "react-bootstrap/esm/Button";
import Modal from "react-bootstrap/esm/Modal";
import { useState, useEffect } from "react";
import axios from 'axios';


const ButtonAddPlaylist = ({setPlaylists}) => {
    
    const [show, setShow] = useState(false);
    const [title, setTitle] = useState('');
    const [selectedSongs, setSelectedSongs] = useState([]);
    const [songs, setSongs] = useState([]);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleSongSelection = (songId) => {
        if (selectedSongs.includes(songId)) {
            // filter creates a new song without the songId
            setSelectedSongs(selectedSongs.filter(id => id !== songId));
        } else {
            // to existing songs add new songId
            setSelectedSongs([...selectedSongs, songId]);
        }
    }

    // get songs with useEffect (componentDidMount)
    useEffect(() => {
        axios.get('http://localhost:8000/music/songs/')
            .then((response) => {
                setSongs(response.data);
            })
            .catch((error) => {
                console.error('Error fetching data: ', error);
            });
    } , []);

    const handleAdd = () => {
        axios.post('http://localhost:8000/music/playlists/', {
            title: title,
            songs_ids: selectedSongs
        })
        .then((response) => {
            console.log(response.data);
            setPlaylists(prevPlaylists => [...prevPlaylists, response.data]);
            handleClose();
            setTitle('');
        })
        .catch((error) => {
            console.error('Error creating playlist: ', error);
        });
    }
    
    return (
    <>
        <Button 
            variant="success"
            onClick={handleShow}
        >
            Add Playlist
        </Button>
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
            <Modal.Title>Add Playlist</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div>
                    <label>Title:</label>
                    <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
                </div>
                <div>
                    <label>Songs:</label>
                    {songs.map(song => (
                        <div key={song.id}>
                        <label>
                            <input type="checkbox" onChange={() => handleSongSelection(song.id)} />
                            {song.title} - {song.artist}
                        </label>
                    </div>
                    ))}
                </div>
            </Modal.Body>
            <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
                Close
            </Button>
            <Button variant="primary" onClick={handleAdd}>
                Add
            </Button>
            </Modal.Footer>
        </Modal>
    </>
    );
}

export default ButtonAddPlaylist;