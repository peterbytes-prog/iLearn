# iLearn
=

# Live Demo at [Link](http://ec2-user@ec2-35-183-131-115.ca-central-1.compute.amazonaws.com "iLearn").


# How to run

### Local
In the terminal run `python manage.py runserver`
* Note: you may need to run migration `python manage.py migrate`
- `python manage.py loaddata auth.json`
- `python manage.py loaddata instructors.json`
- `python manage.py loaddata students.json`
- `python manage.py loaddata subjects.json`
- `python manage.py loaddata courses.json`
- `python manage.py loaddata others.json`
- `python manage.py loaddata assignments.json`

### Docker-compose
In the terminal run `docker-compose -d --build`

* Note: you may need to wait few second to for the app to load all neccesary Fixtures data.

### Testing

In the terminal run `python manage.py test`

* Note: there are 51 unit test and the process may take up to 3-10mins


### Test Users
- Instructor:
-- username: Emiliarose
-- password: Scentlysmooth
- Student:
-- username: evenbaker
-- password: LostfullyDry

* Note: instructor access can only be granted by admin from admin page.


## App Fixtures
=

- User login, authentication & profile management
- Instructors can add subjects, courses and assignments
- Rich Text Editor for adding detail subjects, courses and assignments
- Students can manage their courses enrollments
- Students can live chats with other students that are enrolled in the same course (websocket integrated using python daphnee, channels, redis )
- Students take course test and review past tests

* see doc file for necessary images


## Database Schema
![Alt text](https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/iLearn%20site%20map%20-%20API%20flowchart%20example.svg)
<img src="https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/iLearn%20site%20map%20-%20API%20flowchart%20example.svg">


## Database Schema
![Alt text](https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/ilearn%20database%20schema.svg)
<img src="https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/ilearn%20database%20schema.svg">
