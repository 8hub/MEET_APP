import React from "react";
import logo from '../assets/images/logo512.png';  
import EntryNavBar from "./EntryNavBar";

const EntryPage = () => {
  return (
    <div className="entry-page">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          The time has come to <b>Meet App</b>!
        </p>
        <EntryNavBar />
      </div>
  )
}

export default EntryPage;