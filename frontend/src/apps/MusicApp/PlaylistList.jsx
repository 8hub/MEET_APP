import { useState } from 'react';
import Table from 'react-bootstrap/Table'
import PlaylistRow from './PlaylistRow'

//temp data - will be fetched from backend
const playlists = [
  {
      "id": 1,
      "songs": [
          {
              "id": 1,
              "added_by": null,
              "title": "Dynamite",
              "artist": "Dynamo",
              "url_field": "http://music.mc",
              "add_date": "2024-04-27T11:22:30.608465+02:00"
          },
          {
              "id": 2,
              "added_by": {
                  "id": 1,
                  "username": "user",
                  "email": "user@gmail.com"
              },
              "title": "Ancient vase",
              "artist": "Vasco",
              "url_field": "http://somevase.com",
              "add_date": "2024-05-02T15:44:48.746404+02:00"
          }
      ],
      "created_by": {
          "id": 1,
          "username": "user",
          "email": "user@gmail.com"
      },
      "songs_count": 2,
      "title": "Stomethisng",
      "anonymous": false,
      "add_date": "2024-05-02T15:45:16.740139+02:00",
      "last_modified": "2024-05-02T15:45:16.740139+02:00"
  },
  {
      "id": 2,
      "songs": [
          {
              "id": 1,
              "added_by": null,
              "title": "Dynamite",
              "artist": "Dynamo",
              "url_field": "http://music.mc",
              "add_date": "2024-04-27T11:22:30.608465+02:00"
          },
          {
              "id": 2,
              "added_by": {
                  "id": 1,
                  "username": "user",
                  "email": "user@gmail.com"
              },
              "title": "Ancient vase",
              "artist": "Vasco",
              "url_field": "http://somevase.com",
              "add_date": "2024-05-02T15:44:48.746404+02:00"
          }
      ],
      "created_by": {
          "id": 2,
          "username": "user1",
          "email": "example@mail.com"
      },
      "songs_count": 2,
      "title": "All for one",
      "anonymous": false,
      "add_date": "2024-05-02T15:53:29.978900+02:00",
      "last_modified": "2024-05-02T15:53:29.978900+02:00"
  }
]

const PlaylistList = () => {
  const [open, setOpen] = useState(false);

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
            <PlaylistRow playlist={playlist} open={open} setOpen={setOpen}/>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default PlaylistList;