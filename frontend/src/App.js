import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.scss';
import EntryPage from './components/EntryPage';
import MeetApp from './apps/MeetApp/MeetApp';
import MusicApp from './apps/MusicApp/MusicApp';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<EntryPage />} />
        <Route path="/meetapp" element={<MeetApp />} />
        <Route path="/musicapp" element={<MusicApp />} />
      </Routes>
    </Router>
  );
}

export default App;
