import React, {useContext} from 'react';
import AppButton from './AppButton';
import LoginModal from './LoginModal';
import LogoutButton from './LogoutButton';
import RegisterModal from './RegisterModal';
import { AuthContext } from '../auth';

const EntryNavBar = () => {
  const { state } = useContext(AuthContext);
  return (
    <>
      <div>
        <AppButton buttonName='MeetApp' navigateUrl={"/meetapp"}/>
        <AppButton buttonName='MusicApp' navigateUrl={"/musicapp"}/>
      </div>
      <div>
        {state.isAuthenticated ? (
          <LogoutButton /> 
        ) : (
          <>
          <div className='entry-page-auth-nav'>
            <LoginModal/>
            <RegisterModal/>
          </div>
          </>
        )}
      </div>
    </>
  );
};

export default EntryNavBar;