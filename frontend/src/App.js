import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.scss';
import EntryPage from './components/EntryPage';
import MeetApp from './apps/MeetApp/MeetApp';
import MusicApp from './apps/MusicApp/MusicApp';
import { NotificationProvider } from './notification/NotificationContext';


function App() {
  return (
    <NotificationProvider>
      <Router>
        <Routes>
          <Route path="/" element={<EntryPage />} />
          <Route path="/meetapp" element={<MeetApp />} />
          <Route path="/musicapp" element={<MusicApp />} />
        </Routes>
      </Router>
    </NotificationProvider>
  );
}

export default App;
