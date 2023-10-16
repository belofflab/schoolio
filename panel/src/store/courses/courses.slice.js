import { createSlice } from '@reduxjs/toolkit';

import { getCourses } from './courses.actions';

const courses = localStorage.getItem('courses')
    ? JSON.parse(localStorage.getItem('courses'))
    : []


const initialState = {
    loading: false,
    courses,
    error: null,
    success: false,
}

const courseSlice = createSlice({
    name: 'course',
    initialState,
    reducers: {},
    extraReducers: {
        [getCourses.pending]: (state) => {
            state.loading = true
            state.error = null
        },
        [getCourses.fulfilled]: (state, { payload }) => {
            state.loading = false
            state.success = true
            state.courses = payload
        },
        [getCourses.rejected]: (state, { payload }) => {
            state.loading = false
            state.error = payload
        },
    },
})

const {reducer} = courseSlice;

export default reducer;