import React from 'react';
// import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const AppButton = ({buttonName }) => {
  return (
      <Button
        variant="outline-light"
        style={{margin: '5px'}}
        className='btn btn-custom btn-lg'
      >{buttonName}</Button>
  );
};

export default AppButton;