import React, {useContext} from "react";
import { AuthContext } from "../../auth";
import TopBar from "../../components/TopBar";
import TestButton from "./components/TestButton";

const MeetApp = () => {
  const { state } = useContext(AuthContext);

  return (
    <div className="meetapp-page">
      <TopBar title="MeetApp" />
      <span>{state.isAuthenticated ? "Logged in" : ""}</span>
      <TestButton message="This is a test notification" variant="info" />
      <TestButton message="This is a success notification" variant="success" />
      <TestButton message="This is a warning notification" variant="warning" />
      <TestButton message="This is an error notification" variant="danger" />
    </div>
  );
}
export default MeetApp;