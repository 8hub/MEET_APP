import React, {useContext} from "react";
import { AuthContext } from "../auth";
import LoginModal from "../components/LoginModal";
import LogoutButton from "../components/LogoutButton";

const TopBar = ({title}) => {
  const { state } = useContext(AuthContext);

  return (
    <div className="top-bar">
      <h1>{title}</h1>
      <span>{state.isAuthenticated ? <LogoutButton /> : <LoginModal/>}</span>
    </div>
  );
}

export default TopBar;