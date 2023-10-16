import { configureStore } from '@reduxjs/toolkit'

import authSlice from './auth/auth.slice'
import courseSlice from './courses/courses.slice'

export default configureStore({
    reducer: {
        auth: authSlice,
        course: courseSlice
    }
})