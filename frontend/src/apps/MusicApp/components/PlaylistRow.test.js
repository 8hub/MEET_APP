import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import PlaylistRow from './PlaylistRow';
import ModalDeletePlaylist from './ModalDeletePlaylist';

jest.mock('./ModalDeletePlaylist', () => ({ playlist, setPlaylists }) => (
  <button onClick={() => setPlaylists([])}>Delete Playlist</button>
));

const mockPlaylist = {
  id: 1,
  title: 'Playlist 1',
  created_by: { username: 'User 1' },
  add_date: '2023-05-15T00:00:00Z',
  songs: [
    { title: 'Song 1', artist: 'Artist 1', url_field: 'http://example.com/song1' },
    { title: 'Song 2', artist: 'Artist 2', url_field: 'http://example.com/song2' }
  ]
};

test('renders PlaylistRow component with correct data', () => {
  const setPlaylists = jest.fn();

  render(<PlaylistRow playlist={mockPlaylist} setPlaylists={setPlaylists} />);

  expect(screen.getByText('Playlist 1')).toBeInTheDocument();
  expect(screen.getByText('User 1')).toBeInTheDocument();
  expect(screen.getByText('2023-05-15')).toBeInTheDocument();
  expect(screen.getByText('Show')).toBeInTheDocument();
  expect(screen.queryByText('Hide')).not.toBeInTheDocument();
});

test('toggles song list visibility when the show/hide songs button is clicked', async () => {
    const setPlaylists = jest.fn();
  
    render(<PlaylistRow playlist={mockPlaylist} setPlaylists={setPlaylists} />);
  
    const showButton = screen.getByText('Show');
    fireEvent.click(showButton);
  
    await waitFor(() => {
      expect(screen.getByText('Hide')).toBeInTheDocument();
      expect(screen.getByText('Song 1')).toBeVisible();
      expect(screen.getByText('Artist 1')).toBeVisible();
      expect(screen.getByText('http://example.com/song1')).toBeVisible();
    });
  
    const hideButton = screen.getByText('Hide');
    fireEvent.click(hideButton);
  
    await waitFor(() => {
      expect(screen.getByText('Show')).toBeInTheDocument();
    });
  });

  test('deletes the playlist when the delete button is clicked', async () => {
    const setPlaylists = jest.fn();
  
    // Pass handleShow prop to mock delete functionality
    render(<PlaylistRow playlist={mockPlaylist} setPlaylists={setPlaylists} />);
  
    // Find the "Delete Playlist" button and click it
    const deleteButton = screen.getByText('Delete Playlist');
    fireEvent.click(deleteButton);
  
    // Wait for the setPlaylists function to be called
    await waitFor(() => {
      expect(setPlaylists).toHaveBeenCalledWith([]);
    });
  });