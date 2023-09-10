import React, { useEffect, useState } from 'react';

import {
  Avatar, Button, TextField,
  FormControlLabel, Checkbox, Link,
  Grid, Box, Typography, Container, CircularProgress
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

import Copyright from '../Copyright';

import { useDispatch, useSelector } from 'react-redux';
import { userSignup, userVerify } from '../../store/auth/auth.actions';

export default function SignUp({ onRegisterClick, handleModal }) {

  const [customError, setCustomError] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [authFormData, setAuthFormData] = useState({});
  const [verificationCode, setVerificationCode] = useState('');
  const { success, loading, error, userInfo } = useSelector((state) => state.auth);


  useEffect(() => {
    if (success) {
      if (userInfo) {
        handleModal(false)
      }
      else {
        setShowCodeInput(true);
      }
    }
    if (error) {
      setCustomError(error);
    }
  }, [setCustomError, success, error])



  const dispatch = useDispatch()
  const handleSubmit = (event) => {
    event.preventDefault();

    const data = new FormData(event.currentTarget);
    setAuthFormData({ "idx": data.get("idx"), "email": data.get("email"), "password": data.get("password") })
    const password = data.get('password');

    if (!password.length) {
      setCustomError('Пожалуйста введите пароль')
      return;
    }

    if (!/^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})/.test(password)) {
      setCustomError('Введённый вами пароль ненадежный')
      return;
    }

    dispatch(userSignup({ idx: data.get('idx'), password: password }))
  };

  const handleVerificationSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const otp = data.get('otp');

    dispatch(userVerify({ idx: authFormData.idx, password: authFormData.password, otp: otp }))
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        {loading ? (
          <CircularProgress />
        ) : showCodeInput ? (
          <Box component="form" noValidate onSubmit={handleVerificationSubmit} sx={{ mt: 3 }}>
            <TextField
              required
              fullWidth
              label="Введите код подтверждения"
              id='otp'
              name='otp'
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value)}
            />
            <Button type="submit" variant="contained" sx={{ mt: 3 }}>
              Подтвердить
            </Button>
          </Box>
        ) : (
          <Box>
            <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Регистрация
            </Typography>
            <Typography component="span" variant="caption" sx={{ color: 'red' }}>
              {customError}
            </Typography>
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="idx"
                    label="ID пользователя Telegram"
                    name="idx"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    label="Пароль"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={<Checkbox value="allowExtraEmails" color="primary" />}
                    label="Я хочу получать важные уведомления на почту."
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Зарегистрироваться
              </Button>
              <Grid container justifyContent="flex-end">
                <Grid item>
                  <Link onClick={() => onRegisterClick(true)} href="#" variant="body2">
                    Уже есть аккаунт? Войти
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
        )}
      </Box>
      <Copyright sx={{ mt: 5 }} />
    </Container>
  );
}