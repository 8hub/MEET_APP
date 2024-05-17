import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import PlaylistList from './PlaylistList';

// Create a mock adapter instance for axios
const mock = new MockAdapter(axios);

describe('PlaylistList Component', () => {
  const mockPlaylists = [
    {
      id: 1,
      songs: [1, 2, 3],
      created_by: 'User 1',
      songs_count: 3,
      title: 'Playlist 1',
      anonymous: false,
      add_date: '2023-05-15',
      last_modified: '2023-05-16'
    },
    {
      id: 2,
      songs: [4, 5],
      created_by: 'User 2',
      songs_count: 2,
      title: 'Playlist 2',
      anonymous: true,
      add_date: '2023-05-14',
      last_modified: '2023-05-17'
    }
  ];

  const expectedKeys = [
    'id',
    'songs',
    'created_by',
    'songs_count',
    'title',
    'anonymous',
    'add_date',
    'last_modified'
  ];

  test('fetches and displays playlists with the correct structure', async () => {
    // Mock the GET request to return the defined playlists
    mock.onGet('http://localhost:8000/music/playlists/').reply(200, mockPlaylists);

    // Create a mock function for setPlaylists
    const setPlaylists = jest.fn();

    // Render the PlaylistList component with empty playlists and the mock setPlaylists function
    render(<PlaylistList playlists={[]} setPlaylists={setPlaylists} />);

    // Wait for the axios call to complete and the component to update
    await waitFor(() => expect(setPlaylists).toHaveBeenCalledWith(expect.arrayContaining([
      expect.objectContaining({
        id: expect.any(Number),
        songs: expect.any(Array),
        created_by: expect.any(String),
        songs_count: expect.any(Number),
        title: expect.any(String),
        anonymous: expect.any(Boolean),
        add_date: expect.any(String),
        last_modified: expect.any(String)
      })
    ])));

    // Assert that the playlist data is displayed correctly in the document
    mockPlaylists.forEach(playlist => {
      expect(screen.getByText(playlist.title)).toBeInTheDocument();
      expect(screen.getByText(playlist.created_by)).toBeInTheDocument();
      expect(screen.getByText(playlist.add_date)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    // Mock the GET request to return a 500 error
    mock.onGet('http://localhost:8000/music/playlists/').reply(500);

    // Create a mock function for setPlaylists
    const setPlaylists = jest.fn();
    console.error = jest.fn(); // Mock console.error to silence the error in the test output

    // Render the PlaylistList component with empty playlists and the mock setPlaylists function
    render(<PlaylistList playlists={[]} setPlaylists={setPlaylists} />);

    // Wait for the axios call to complete and the component to update
    await waitFor(() => expect(console.error).toHaveBeenCalled());

    // Assert that setPlaylists was not called due to the error
    expect(setPlaylists).not.toHaveBeenCalled();
  });
});
