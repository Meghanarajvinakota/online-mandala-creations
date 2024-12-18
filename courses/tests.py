from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Course
from django.utils import timezone


# ------------ MODEL TESTING ------------

class TestCategory(TestCase):
    """Tests the Category model in the courses app."""

    def setUp(self):
        """
        Makes a sample Category object
        """

        name = "test_category"
        display_name = "test_category_display"
        category1 = Category.objects.create(
            name=name,
            display_name=display_name
            )

        category1.save()

    def test_str(self):
        """Tests the string method on the category."""
        # Retrieves the most recently created category and gets its string
        category1 = Category.objects.latest('pk')
        category_string = str(category1.name)

        # Cofirms the category string is correct.
        self.assertEqual((category_string), (category1.name))


class TestCourse(TestCase):
    """Tests the Course model in the courses app."""

    def setUp(self):
        """
        Makes a sample Course object
        """

        name = "test_course"
        description = "test_course_description"
        price = '999.99'
        date_created = timezone.now()
        course1 = Course.objects.create(
            name=name,
            description=description,
            price=price,
            date_created=date_created
            )

        course1.save()

    def test_str(self):
        """Tests the string method on the course."""
        # Retrieves the most recently created course and gets its string
        course1 = Course.objects.latest('pk')
        course_string = str(course1.name)

        # Cofirms the course string is correct.
        self.assertEqual((course_string), (course1.name))


# ------------ VIEWS TESTING ------------

class CourseViewTestCase(TestCase):
    """
    Test case for testing course views.
    """

    def setUp(self):
        """
        Creates two sample users, one of whom has staff & superuser
        privileges (testUserStaff) and another who does not (testUser).
        Then, creates a sample course.
        """

        username1 = "testUser"
        email1 = "testuser@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        username2 = "testUserStaff"
        email2 = "testuser2@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        user1 = User.objects.create(
            username=username1,
            email=email1,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

        user2 = User.objects.create(
            username=username2,
            email=email2,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

        user2.is_staff = True
        user2.is_superuser = True

        user1.save()
        user2.save()

        name = "test_course"
        description = "test_course_description"
        price = '999.99'
        date_created = timezone.now()
        course1 = Course.objects.create(
            name=name,
            description=description,
            price=price,
            date_created=date_created
            )

        course1.save()

    def test_courses_render_context(self):
        """
        Tests that the courses page is rendered properly
        """

        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'courses/courses.html', 'base.html'
            )

        # Checks whether the context item is passed in
        self.assertTrue(response.context['courses'])

    def test_edit_course_render_form(self):
        """
        Checks that the edit course page cannot be accessed by non-superusers.
        Tests the url path by passing in the primary key of new test
        course. Checks that the course detail page is rendered properly.
        Checks that the course detail view matches the test course passed
        into the url.
        """

        # Get the most recently created user (testUserStaff)
        test_user_staff = User.objects.latest('date_joined')

        # Get the second most recently created user (testUser)
        test_user = User.objects.filter().order_by('-pk')[1]

        # Check that the two users are correctly retrieved
        self.assertEqual(test_user_staff.username, 'testUserStaff')
        self.assertEqual(test_user.username, 'testUser')

        # Tests the url path
        course1 = Course.objects.latest('pk')

        # Log in as testUser (no staff privileges)
        self.client.force_login(test_user)

        # Try to access edit course page (staff-only)
        response = self.client.get(f'/courses/edit/{course1.pk}/')

        # Check that page access is not granted
        self.assertNotEqual(response.status_code, 200)

        # Check that we do not reach the edit course page
        self.assertTemplateNotUsed('courses/edit_course.html')

        # Log in as testUserStaff (has staff privileges)
        self.client.force_login(test_user_staff)

        # Try to access course details page (staff-only)
        response = self.client.get(f'/courses/edit/{course1.pk}/')

        # Check that page access is granted
        self.assertEqual(response.status_code, 200)

        # Checks that the page renders correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'courses/edit_course.html',
            'base.html'
            )

        # Get the most recent course
        # (should be test_course that was just created)
        courseToUpdate = Course.objects.latest('date_created')

        # update the course
        response = self.client.post((
            f'/courses/edit/{courseToUpdate.pk}/'
            ), {
            'name': "test_course_updated",
            'description': "test_course_description_updated",
            'price': '9.99',
            'date_created': timezone.now(),
            })

        # Get the most recent post
        # (should be test_course_updated that was just updated)
        newTestCourse = Course.objects.latest('date_created')

        course_string_name = str(newTestCourse.name)
        course_string_description = str(newTestCourse.description)
        course_string_price = str(newTestCourse.price)

        # Check that the post has been successfuly updated
        self.assertEqual(
            (course_string_name), ("test_course_updated")
            )
        self.assertEqual(
            (course_string_description), ("test_course_description_updated")
            )
        self.assertEqual(
            (course_string_price), ("9.99")
            )

    def test_add_course_render_form(self):
        """
        Checks that the add course page cannot be accessed by non-superusers.
        Checks that the page is rendered properly.
        Creates a new test course using the page form.
        Tests that the course was created successfully.
        """

        # Get the most recently created user (testUserStaff)
        test_user_staff = User.objects.latest('date_joined')

        # Get the second most recently created user (testUser)
        test_user = User.objects.filter().order_by('-pk')[1]

        # Check that the two users are correctly retrieved
        self.assertEqual(test_user_staff.username, 'testUserStaff')
        self.assertEqual(test_user.username, 'testUser')

        # Get the object's pk
        course1 = Course.objects.latest('pk')

        # Log in as testUser (no staff privileges)
        self.client.force_login(test_user)

        # Try to access add course page (staff-only)
        response = self.client.get(f'/courses/add/')

        # Check that page access is not granted
        self.assertNotEqual(response.status_code, 200)

        # Check that we do not reach the add course page
        self.assertTemplateNotUsed('courses/add_course.html')

        # Log in as testUserStaff (has staff privileges)
        self.client.force_login(test_user_staff)

        # Try to access add course page (staff-only)
        response = self.client.get(f'/courses/add/')

        # Check that page access is granted
        self.assertEqual(response.status_code, 200)

        # Checks that the page renders correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'courses/add_course.html',
            'base.html'
            )

        # Get the ID of the most recently created course object
        originalCourse = Course.objects.latest('pk')
        originalCourseId = originalCourse.pk

        # Create a new test course using the page form
        response = self.client.post(('/courses/add/'), {
            'name': 'test_course_created',
            'description': 'test_course_description_created',
            'price': '99.99',
            'date_created': timezone.now()
            })

        # Get the most recent course object
        # (should be test_course_created that was just created)
        newTestCourse = Course.objects.latest('pk')
        newTestCoursetId = newTestCourse.pk

        # Check that the most recent course created is
        # not the original course, meaning a new one
        # was successfully created
        self.assertNotEqual((originalCourseId), (newTestCoursetId))

        # Check that the most recently created object
        # is our test course object
        self.assertEqual(
            'test_course_created', Course.objects.latest('pk').name
            )

    def test_delete_course_render_form(self):
        """
        Checks that courses cannot be deleted by non-superusers.
        Deletes the test object.
        Checks that the test object was successfully deleted.
        """

        # Get the most recently created user (testUserStaff)
        test_user_staff = User.objects.latest('date_joined')

        # Get the second most recently created user (testUser)
        test_user = User.objects.filter().order_by('-pk')[1]

        # Check that the two users are correctly retrieved
        self.assertEqual(test_user_staff.username, 'testUserStaff')
        self.assertEqual(test_user.username, 'testUser')

        # Get the most recently created course object
        courseToDelete = Course.objects.latest('pk')

        # Get the to-be-deleted course object's ID
        deletedCourseId = (courseToDelete.pk)

        # Log in as testUser (not superuser)
        self.client.force_login(test_user)

        # Attempt to delete the course object using the delete view
        response = self.client.post(
            f'/courses/courses/delete/{courseToDelete.pk}/'
            )

        # Check that access is denied
        self.assertNotEqual(response.status_code, 200)

        # Log in as testUserStaff (superuser)
        self.client.force_login(test_user_staff)

        # Delete the course object using the delete view
        response = self.client.post(
            f'/courses/delete/{courseToDelete.pk}/', follow=True
            )
        self.assertEqual(response.status_code, 200)

        # Check if there are any course objects in the database,
        # if not, that means that the deletion was successful
        if Course.objects.exists():
            # If there are course objects remaining, we need to
            # check that the one we tried to delete has been deleted.
            # Get the ID of the last course object in the database
            newLastCourse = Course.objects.latest('pk')
            newLastCourseId = newLastCourse.pk

            # Check if the last course object in the database is the
            # same one that we tried to delete, if not, that
            # means the deletion was successful
            self.assertNotEqual(deletedCourseId, newLastCourseId)