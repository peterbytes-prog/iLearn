# iLearn

#Description
An e-learning platform application with content management system (CMS), live chat, student test and grading.

# Demo
Live Demo At [Link](http://ec2-user@ec2-35-183-131-115.ca-central-1.compute.amazonaws.com "iLearn").

<img src="./docs/home.png" />
<img src="./docs/enroll.png" />
<img src="./docs/course_content_view.png" />
<img src="./docs/course_create.png" />
<img src="./docs/create_assignment_content.png" />
<img src="./docs/instructor_courses_page.png" />
<img src="./docs/manage_course_module.png" />
<img src="./docs/manage_questions.png" />
<img src="./docs/student_courses__list.png" />
<img src="./docs/student_test_page.png" />
<img src="./docs/student_test_attempts_reveiw.png" />
<img src="./docs/user_profile.png" />

<section>
  <h2>Technologies Used</h2>
  <div>
    <ul>
      <li>
        Bootstrap
      </li>
      <li>
        HTML5
      </li>
      <li>
        CSS
      </li>
      <li>
        Python Django
      </li>
      <li>
        DRF
      </li>
      <li>
        MySQL
      </li>
      <li>
        Javascript
      </li>
      <li>
        jQuery
      </li>
    </ul>
  </div>
</section>
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


<ul class="list-inline">
  <li class="list-inline-item">
    Login, Register and Authentication Capabilities
  </li>
  <li class="list-inline-item">
    Content Management System (CMS)
  </li>
  <li class="list-inline-item">
    Rich Text Editor for adding detail subjects, courses and assignments
  </li>
  <li class="list-inline-item">
    Live chat
  </li>
  <li class="list-inline-item">
    Student testing and grading
  </li>
  <li class="list-inline-item">
    Admin Management
  </li>
</ul>

* see doc file for necessary images


## Database Schema
![Alt text](https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/iLearn%20site%20map%20-%20API%20flowchart%20example.svg)
<img src="https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/iLearn%20site%20map%20-%20API%20flowchart%20example.svg">


## Database Schema
![Alt text](https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/ilearn%20database%20schema.svg)
<img src="https://raw.githubusercontent.com/snipersenpai/iLearn/main/docs/ilearn%20database%20schema.svg">
