import React, { useEffect, useState } from 'react';
import Course from '../../containers/Course';
import { Typography, Box, Grid, Stack, Button, Link } from '@mui/material';
import BeloffLabImage from "../../assets/images/header_belofflab.png"
import BeloffImage from "../../assets/images/beloff.webp"
import AgeevImage from "../../assets/images/ageev.png"
import UskovImage from "../../assets/images/uskov.png"
import { Telegram, Instagram } from '@mui/icons-material'
export default function Home({ authenticated }) {
    return (
        <Box sx={{
            marginTop: 7,
        }}>
            <Box id="about">
                <Grid container spacing={2}>
                    <Grid item md={6} lg={6}>
                        <Box>
                            <Typography variant='h4' sx={{
                                fontWeight: '600',
                                marginBottom: 1
                            }}>
                                Добро пожаловать в нашу компьютерную академию!
                            </Typography>
                            <Typography variant='p' sx={{ fontSize: 18 }}>
                                Наше <Link href='/'>учебное заведение</Link> специализируется на создании <Link href="#academy">топовых специалистов</Link> в сфере информационных технологий. У нас вы найдете не только образование, но и вдохновение для развития вашей карьеры. Мы предоставляем высококачествное образование и поддержку, которые помогут вам стать лидером в мире IT-инноваций.
                            </Typography>
                                <Stack spacing={2} direction="row" sx={{marginTop: 7}}>
                                    <Button variant="text" color='success'>Начинающим</Button>
                                    <Button variant="outlined" color='success'>Экспертам</Button>
                                </Stack>
                        </Box>
                    </Grid>
                    <Grid item md={6} lg={6}>
                        <Box component="img" src={BeloffLabImage}></Box>
                        <Typography variant='h5'>
                            ЗДЕСЬ БУДЕТ ФОРМА ЗАЯВКИ Вместо изображения
                        </Typography>
                    </Grid>
                </Grid>
            </Box>

            <Box id="mentors">
                <Typography variant='h4' sx={{
                    textAlign: 'center',
                    marginTop: 7,
                    fontWeight: '600',
                    marginBottom: 5
                }}>Наши менторы (учителя)</Typography>
                <Grid container spacing={2} sx={{ marginTop: 7 }}>
                    <Grid item md={6} lg={6}>
                        <Box component='img' src={BeloffImage} sx={{ width: '80%', borderRadius: 40 }}></Box>
                    </Grid>
                    <Grid item md={6} lg={6}>
                        <Typography variant='h5' sx={{ marginBottom: 2 }}>
                            <b>Константин Белов</b> - ведущий разработчик <Link href="https://hermesinternational.ru" target="_blank">Hermes International.</Link>
                        </Typography>
                        <Typography variant='p' >
                            <b>Hermes International</b> - компания, которая специализируется на международной пересылке товаров, позволяя вам покупать на американских площадках онлайн и получать заказы с минимальными затратами и максимальным комфортом.
                        </Typography>
                        <Box sx={{ marginTop: 2 }}>
                            <Typography variant='p' sx={{ fontWeight: 700 }}>Связаться с ментором:</Typography>
                            <Stack direction="row" alignItems="center" spacing={4} sx={{ marginTop: 2 }}>
                                <Link href="https://t.me/belofflab" target="_blank"><Telegram fontSize="large" /></Link>
                                <Link href="https://instagram.com/belofflab" target="_blank"><Instagram fontSize='large' /></Link>
                            </Stack>
                        </Box>
                    </Grid>
                </Grid>
                <Grid wrap={window.screen.width < 899 ? 'wrap-reverse' : ''} container spacing={2} sx={{ marginTop: 7 }}>
                    <Grid item md={6} lg={6}>
                        <Typography variant='h5' sx={{ marginBottom: 2 }}>
                            <b>Никита Усков</b> - основатель <Link href="https://belofflab.com/vpn" target="_blank">Beloff Lab Secure.</Link>
                        </Typography>
                        <Typography variant='p' >
                            <b>Beloff Lab Secure</b> - проект, обеспечивающий полную анонимизацию и безопасность в сети. Иначе говоря, VPN.
                        </Typography>
                        <br />
                        <br />
                        <Typography variant='p' >
                            P.S. Сейчас проект в заморозке...
                        </Typography>
                        <Box sx={{ marginTop: 2 }}>
                            <Typography variant='p' sx={{ fontWeight: 700 }}>Связаться с ментором:</Typography>
                            <Stack direction="row" alignItems="center" spacing={4} sx={{ marginTop: 2 }}>
                                <Link href="https://t.me/belofflab" target="_blank"><Telegram fontSize="large" /></Link>
                                <Link href="https://instagram.com/belofflab" target="_blank"><Instagram fontSize='large' /></Link>
                            </Stack>
                        </Box>
                    </Grid>
                    <Grid item md={6} lg={6}>
                        <Box component='img' src={UskovImage} sx={{ width: '80%', borderRadius: 40 }}></Box>
                    </Grid>
                </Grid>
                <Grid container spacing={2} sx={{ marginTop: 7 }}>
                    <Grid item md={6} lg={6}>
                        <Box component='img' src={AgeevImage} sx={{ width: '70%', borderRadius: 40 }}></Box>
                    </Grid>
                    <Grid item md={6} lg={6}>
                        <Typography variant='h5' sx={{ marginBottom: 2 }}>
                            <b>Даниил Агеев</b> - Scratch Senior Developer
                        </Typography>
                        <Typography variant='p' >
                            Обучает Scratch, да и в принципе всё... Может обучить трогаться на механике!
                        </Typography>
                        <Box sx={{ marginTop: 2 }}>
                            <Typography variant='p' sx={{ fontWeight: 700 }}>Связаться с ментором:</Typography>
                            <Stack direction="row" alignItems="center" spacing={4} sx={{ marginTop: 2 }}>
                                <Link href="https://t.me/belofflab" target="_blank"><Telegram fontSize="large" /></Link>
                                <Link href="https://instagram.com/belofflab" target="_blank"><Instagram fontSize='large' /></Link>
                            </Stack>
                        </Box>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    );
}