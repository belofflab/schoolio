import http from '../../http';
import { createAsyncThunk } from '@reduxjs/toolkit'

export const getCourses = createAsyncThunk(
  'course/getCourses',
  async (_, { rejectWithValue }) => {
    try {

      const { data } = await http.get("courses/")

      if(data?.status_code !== 200) {
        return rejectWithValue(data.detail)
      }


      localStorage.setItem('courses', JSON.stringify(data))

      return data
    } catch (error) {
      return rejectWithValue(error.response.statusText)
    }
  }
)
