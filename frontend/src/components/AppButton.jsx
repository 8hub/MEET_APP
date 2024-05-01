import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const AppButton = ({ buttonName, navigateUrl }) => {
  const navigate = useNavigate();
  const navigateTo = () => {
    navigate(navigateUrl);
  }
  return (
      <Button
        variant="outline-light"
        style={{margin: '5px'}}
        className='btn btn-custom btn-lg'
        onClick={navigateTo}
      >{buttonName}</Button>
  );
};

export default AppButton;