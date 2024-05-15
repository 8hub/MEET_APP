import { useState, useContext } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import axios from 'axios';
import { AuthContext } from '../../../auth';
import DeletePlaylistButton from './DeletePlaylistButton';

const ButtonDeletePlaylist = ({playlist, setPlaylists}) => {
    const { state } = useContext(AuthContext);
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const handleDelete = () => {
        axios.delete(`http://localhost:8000/music/playlists/${playlist.id}/`)
            .then(() => {
                setPlaylists(prevPlaylists => prevPlaylists.filter(p => p.id !== playlist.id));
                handleClose();
            })
            .catch((error) => {
                console.error('Error deleting playlist: ', error);
                handleClose();
            });
    }
    
    // disabled if the user is not logged in or if the user is not the creator of the playlist
    const isDisabledDelete = state.isAuthenticated ? (JSON.stringify(state.user) !== JSON.stringify(playlist.created_by)) : true;
    
    return (
        <>
            <DeletePlaylistButton
                isDisabledDelete={isDisabledDelete}
                handleShow={handleShow}
            />
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Delete Playlist</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Are you sure you want to delete this playlist?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="danger" onClick={handleDelete}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default ButtonDeletePlaylist;