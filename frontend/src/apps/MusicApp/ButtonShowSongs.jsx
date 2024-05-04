import Button from 'react-bootstrap/Button';

const ButtonShowSongs = ({open, setOpen}) => {
  return (
    <Button
      variant="outline-light"
      size="md"
      onClick={() => setOpen(!open)}
    >
      {open ? 'Hide' : 'Show'}
    </Button>
  );
}

export default ButtonShowSongs;