import React, {useContext} from "react";
import { AuthContext } from "../../auth";
import TopBar from "../../components/TopBar";


const MusicApp = () => {
  const { state } = useContext(AuthContext);

  return (
    <div className="musicapp-page">
      <TopBar title="MusicApp" />
      <span>{state.isAuthenticated ? "Logged in" : ""}</span>
    </div>
  );
}
export default MusicApp;