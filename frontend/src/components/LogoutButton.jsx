import React, {useContext} from 'react';
import Button from 'react-bootstrap/Button';
import {logout, AuthContext } from '../auth';

const LogoutButton = () => {
  const {dispatch} = useContext(AuthContext);

  const handleLogout = (e) => {
    e.preventDefault();
    // send axios request to backend
    logout(dispatch);
  };
  
  return (
      <Button 
        variant='primary'
        type='submit'
        className="btn-link btn-link-custom"
        onClick={handleLogout}
      >
        Logout
      </Button>
  );
}

export default LogoutButton;