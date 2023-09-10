import React from 'react';
import { Box, Button, Modal } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  borderRadius: 7
};

const ModalWindow = ({ children, title, open, handleModal }) => {

  return (
    <div>
      <Button sx={{ color: 'white' }} onClick={() => handleModal(true)}>{title}</Button>
      <Modal
        open={open}
        onClose={() => handleModal(false)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          {children}
        </Box>
      </Modal>
    </div>
  );
}


export default ModalWindow;