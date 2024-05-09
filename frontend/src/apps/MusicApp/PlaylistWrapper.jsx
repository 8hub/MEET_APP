import { useState } from "react";
import PlaylistList from "./PlaylistList";
import ButtonAddPlaylist from "./ButtonAddPlaylist";

const PlaylistWrapper = () => {
  const [playlists, setPlaylists] = useState([]);

  return (
    <div className="playlist-wrapper">
      <PlaylistList playlists={playlists} setPlaylists={setPlaylists} />
      <ButtonAddPlaylist setPlaylists={setPlaylists} />
    </div>
  );
}

export default PlaylistWrapper;