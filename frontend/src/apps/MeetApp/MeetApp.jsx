import React, {useContext} from "react";
import { AuthContext } from "../../auth";
import TopBar from "../../components/TopBar";
import PlaylistWrapper from "./PlaylistWrapper";

const MeetApp = () => {
  const { state } = useContext(AuthContext);

  return (
    <div className="meetapp-page">
      <TopBar title="MeetApp" />
      <span>{state.isAuthenticated ? "Logged in" : ""}</span>
      <PlaylistWrapper />
    </div>
  );
}
export default MeetApp;