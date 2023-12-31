import React, { useEffect } from 'react';

import { useDispatch, useSelector } from 'react-redux'
import { getCourses } from '../../store/courses/courses.actions'

function Course({authenticated}) {

    const dispatch = useDispatch();
    const { loading, error, courses } = useSelector((state) => state.course)

    useEffect(() => {
        console.log(authenticated)
        if (authenticated) {
            dispatch(getCourses())
            console.log(courses)
        }

    }, [dispatch, authenticated])


    if (loading) {
        return <p>loading</p>
    }

    if (error) {
        return <p>Something went wrong</p>
    }


    return (
        <div id="courses">
            {courses.map(course => (
                <div className="course" key={course.idx}>
                    <p>{course.idx}</p>
                </div>
            ))}
        </div>
    );
}

export default Course;