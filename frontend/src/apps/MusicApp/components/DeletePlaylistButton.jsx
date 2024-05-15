import React from 'react';
import { Button } from 'react-bootstrap';
import { useNotification } from '../../../notification/NotificationContext';

const DeletePlaylistButton = ({ isDisabledDelete, handleShow }) => {
    const showNotification = useNotification();

    const handleDisabledClick = () => {
        showNotification("To delete playlist you have to be playlist creator", "danger");
    };

    return (
        <div style={{ position: 'relative', display: 'inline-block' }}>
            <Button
                className='btn-delete-playlist'
                variant='danger'
                onClick={handleShow}
                disabled={isDisabledDelete}
            >
                Delete
            </Button>
            {isDisabledDelete && (
                <div
                    className='btn-delete-disabled'
                    onClick={handleDisabledClick}
                ></div>
            )}
        </div>
    );
};

export default DeletePlaylistButton;
