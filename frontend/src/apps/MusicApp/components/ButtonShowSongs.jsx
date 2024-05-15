import Button from 'react-bootstrap/Button';

const ButtonShowSongs = ({open, setOpen}) => {
  return (
    <Button
      className="btn-show"
      size="md"
      onClick={() => setOpen(!open)}
    >
      {open ? 'Hide' : 'Show'}
    </Button>
  );
}

export default ButtonShowSongs;