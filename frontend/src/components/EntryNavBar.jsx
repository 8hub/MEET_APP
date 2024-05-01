import React, {useContext} from 'react';
import AppButton from './AppButton';
import LoginModal from './LoginModal';
import LogoutButton from './LogoutButton';
import { AuthContext } from '../auth';

const EntryNavBar = () => {
  const { state } = useContext(AuthContext);
  return (
    <>
      <div>
        <AppButton buttonName='MeetApp' navigateUrl={"/meetapp"}/>
        <AppButton buttonName='SongApp' navigateUrl={"/musicapp"}/>
      </div>
      <div>
        {state.isAuthenticated ? <LogoutButton /> : <LoginModal/>}
      </div>
    </>
  );
};

export default EntryNavBar;