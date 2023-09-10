import { createSlice } from '@reduxjs/toolkit';

import { userLogin, userSignup, userVerify } from './auth.actions';
import { isAuthenticated } from '../../helpers/is_authenticated';

const success = isAuthenticated()

const userToken = localStorage.getItem('userToken')
    ? localStorage.getItem('userToken')
    : null

const userInfo = localStorage.getItem('userInfo')
    ? JSON.parse(localStorage.getItem('userInfo'))
    : null


const initialState = {
    loading: false,
    userInfo,
    userToken,
    error: null,
    success,
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout: (state) => {
            state.success = false
            state.userInfo = {}
            localStorage.clear()
        }   
    },
    extraReducers: {
        [userLogin.pending]: (state) => {
            state.loading = true
            state.error = null
        },
        [userLogin.fulfilled]: (state, { payload }) => {
            state.loading = false
            state.success = true
            state.userInfo = payload
            state.userToken = payload.access_token
        },
        [userLogin.rejected]: (state, { payload }) => {
            state.loading = false
            state.error = payload
        },
        [userSignup.pending]: (state) => {
            state.loading = true
            state.error = null
        },
        [userSignup.fulfilled]: (state, { payload }) => {
            state.loading = false
            state.success = true
        },
        [userSignup.rejected]: (state, { payload }) => {
            state.loading = false
            state.error = payload
        },
        [userVerify.pending]: (state) => {
            state.loading = true
            state.error = null
        },
        [userVerify.fulfilled]: (state, { payload }) => {
            state.loading = false
            state.success = true
            state.userInfo = payload
            state.userToken = payload.access_token
        },
        [userVerify.rejected]: (state, { payload }) => {
            state.loading = false
            state.error = payload
        },
    },
})

const {actions, reducer} = authSlice;

export const { logout } = actions;

export default reducer;