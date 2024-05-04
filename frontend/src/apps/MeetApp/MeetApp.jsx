import React, {useContext} from "react";
import { AuthContext } from "../../auth";
import TopBar from "../../components/TopBar";


const MeetApp = () => {
  const { state } = useContext(AuthContext);

  return (
    <div className="meetapp-page">
      <TopBar title="MeetApp" />
      <span>{state.isAuthenticated ? "Logged in" : ""}</span>
    </div>
  );
}
export default MeetApp;