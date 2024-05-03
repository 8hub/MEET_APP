import { useState } from 'react';
import Table from 'react-bootstrap/Table'
import Button from 'react-bootstrap/Button'
import Collapse from 'react-bootstrap/Collapse'
// import Container from 'react-bootstrap/Container'

const PlaylistList = () => {
  const [open, setOpen] = useState(false);
  const arr = [1, 2, 3];

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
          <tr>
            <td className='column-1'>Playlist 1 - long playlist name</td>
            <td className='column-2'>John Doe</td>
            <td className='column-3 center-text'>2020-01-01</td>
            <td className='column-4 center-text'>
            <Button
              onClick={() => setOpen(!open)}
              aria-controls="collapse-song-list"
              aria-expanded={open}
            >
              View
            </Button>
            </td>
          </tr>
          <Collapse in={open}>
            <div className="collapse-song-list">
              {arr.map(i => (
                <tr>
                  <td>
                    Song title {i}
                  </td>
                  <td>
                    Artist {i}
                  </td>
                  <td>
                    Link {i}
                  </td>
                </tr>
              ))}
            </div>
          </Collapse>
          <tr>
            <td className='column-1'>Playlist 2</td>
            <td className='column-2'>Jane Doe</td>
            <td className='column-3 center-text'>2020-01-02</td>
            <td className='column-4 center-text'>
              <Button variant="primary">View</Button>
            </td>
          </tr>
          <tr>
            <td className='column-1'>Playlist 3</td>
            <td className='column-2'>John Doer</td>
            <td className='column-3 center-text'>2020-01-03</td>
            <td className='column-4 center-text'>
              <Button variant="primary">View</Button>
            </td>
          </tr>
        </tbody>
      </Table>
    </div>
  );
}

export default PlaylistList;