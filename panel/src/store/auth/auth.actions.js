import http from '../../http';
import { createAsyncThunk } from '@reduxjs/toolkit'

export const userLogin = createAsyncThunk(
  'auth/login',
  async ({ idx, password }, { rejectWithValue }) => {
    try {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        },
      }
      const { data } = await http.post(
        'users/signin',{
          idx: idx,
          password: password
        },
        config
      )

      if (data.status_code) {
        if(data.status_code !== 200) {
          return rejectWithValue(data.detail)
        }
      }

      localStorage.setItem('userToken', data.access_token)
      localStorage.setItem('userInfo', JSON.stringify(data))

      return data
    } catch (error) {
      return rejectWithValue(error.response.statusText)
    }
  }
)

export const userSignup = createAsyncThunk(
  'auth/signup',
  async ({ idx, password }, { rejectWithValue }) => {
    try {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        }
      }
      const { data } = await http.post(
        'users/signup', {
        idx: idx,
        password: password
      },
        config
      )

      if (data.status_code !== 200) {
        return rejectWithValue(data?.detail)
      }

      return data
    } catch (error) {
      return rejectWithValue(error.response.data)
    }
  }
)

export const getMe = createAsyncThunk(
  'users/me',
  async ({ token }, { rejectWithValue }) => {
    try {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        },
      }
      const { data } = await http.get(
        `auth/me?token=${token}`,
        config
      )
      localStorage.setItem('userInfo', JSON.stringify(data))
      return data
    } catch (error) {
      return rejectWithValue(error.response.data)
    }
  }
)

export const userVerify = createAsyncThunk(
  'auth/verify',
  async ({ idx, password, otp }, { rejectWithValue }) => {
    try {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        }
      }
      const { data } = await http.post(
        'users/verify', {
        idx: idx,
        password: password,
        otp: otp
      },
        config
      )
      localStorage.setItem('userToken', data.access_token)
      localStorage.setItem('userInfo', JSON.stringify(data))
      return data
    } catch (error) {
      return rejectWithValue(error.response.data)
    }
  }
)