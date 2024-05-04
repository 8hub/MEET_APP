import React, {useContext} from "react";
import { AuthContext } from "../../auth";
import TopBar from "../../components/TopBar";
import PlaylistWrapper from "./PlaylistWrapper";

const MusicApp = () => {
  const { state } = useContext(AuthContext);

  return (
    <div className="musicapp-page">
      <TopBar title="MusicApp" />
      <span>{state.isAuthenticated ? "Logged in" : ""}</span>
      <PlaylistWrapper />
    </div>
  );
}
export default MusicApp;