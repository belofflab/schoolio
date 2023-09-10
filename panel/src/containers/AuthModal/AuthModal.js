import React, { useState } from 'react';

import SignUp from '../../components/SignUp';
import SignIn from '../../components/SignIn';

import ModalWindow from '../ModalWindow'

function AuthModal(props) {

    const [isRegister, setIsRegister] = useState(true);
    const [open, setOpen] = useState(false);
    return (
        <ModalWindow
            open={open}
            handleModal={setOpen}
            children={
                isRegister ?
                    (
                        <SignIn onRegisterClick={setIsRegister} handleModal={setOpen} />
                    ) : (
                        <SignUp onRegisterClick={setIsRegister} handleModal={setOpen} />
                    )
            }
            title='Авторизоваться' />
    );
}

export default AuthModal;