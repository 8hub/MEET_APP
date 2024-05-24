import React, {useState, Fragment} from "react";
import Modal from "react-bootstrap/Modal";
import ModalHeader from "react-bootstrap/ModalHeader";
import ModalBody from "react-bootstrap/ModalBody";
import Button from "react-bootstrap/Button";
import RegisterForm from "./RegisterForm";

const RegisterModal = () => {
  const [show, setShow] = useState(false);
  const handleShow = () => setShow(true);
  const handleClose = () => setShow(false);

  return (
    <Fragment>
      <Button
        onClick={handleShow}
        className="btn-link btn-link-custom"
      >
        Register
      </Button>
    <Modal 
      show={show}
      onHide={handleClose}
      >
      <ModalHeader closeButton>
        <Modal.Title>Register</Modal.Title>
      </ModalHeader>
      <ModalBody>
        <RegisterForm handleClose={handleClose}/>
      </ModalBody>
    </Modal>
    </Fragment>
  );
}

export default RegisterModal;