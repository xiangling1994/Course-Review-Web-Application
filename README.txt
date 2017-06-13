Project Title: Course Review Web Application

Team Members:
	Wenjing Zhu
	Xiang Ling
	Arnold Zoundi

Description: The Course Review Web Application is similar to RateMyProfessor. The difference between these two applications is that RateMyProfessor focuses on professors reviews whereas our project focuses on courses reviews. Our application currently support all courses taught at Dalhousie University. However, it can easily be extended to include other universities. The purpose of this application to provide good, correct, fair and unbiased courses' information and ratings to students. These information will help students make better choices in terms of courses to match their needs for a specific semester.
URL: http://rap-project-dev.us-west-2.elasticbeanstalk.com/
Repository: https://github.com/CSCI2133RAP/rap_project


TESTING GUIDELINES

In order to test this project, the marker will have to consider two group of users which are visitors and registered users.
The marker should be able to perform the following tasks as a visitor:
	- Access "Featured Course Collection"
	- Search all courses for a specific department (e.g: Computer Science) at Dalhousie University
	- Search a specific course by course ID (e.g: CSCI 1100)
	- Access course details
	- Access users' comments on courses
	- unable to see upvotes and downvotes on comments as a visitor
	- Access professors' ratings for a specific course
	- unable to comment and rate as a visitor
	
The marker should be able to perform the following tasks as a registered user:
	- Register as a new user
	- Log in with the new user credentials
	- Access "Featured Course Collection"
	- Search all courses for a specific department (e.g: Computer Science) at Dalhousie University
	- Search a specific course by course ID (e.g: CSCI 1100)
	- Access course details
	- Access users' comments on courses
	- Add comments to courses
	- upvote and downvote comments (each should not allow more than one upvote and downvote on a course for the same user)
	- Access professors' ratings for a specific course
	- Rate a professor for a specific course (should only allow one rating per user)
	- Access user's profile information
	- Delete comments
	- change password
	- Log out


USER DOCUMENTATION

	REGISTRATION FUNCTION
	
	In order to register an account, please follow these steps:
		- Click on Login in the in the navigation bar in the homepage
		- Click on the Register button
		- Provide your username, password and email
		- Click on the Submit button. You have just created an account.

	LOGIN FUNCTION
	
	In order to login to your account, please follow these steps:
		- Click on Login in the in the navigation bar in the homepage
		- Provide your username and password
		- Click on the Submit button. You have just logged in to your account.


	SEARCH FUNCTION
	
	In order to perform a search in the application, please follow these steps in the specified order:
	
		- Make sure you are on the homepage
		- Select the University (e.g: Dalhousie) in the first dropdown menu
		- Click on the search button. Now, you should be able to see the Featured Course Collection for the selected university.
		- To go further, select the subject (e.g: Computer Science) in the second dropdown menu.
		- Click on the search button. Now, you should be able to see the list of all courses for the selected university and subject.
		- To go even further, provide a course ID (e.g.: CSCI 1100) to search for a specific course.
		- Click on the search button. If the course is in the database, the application will return the appropriate result.
		- Click on the green arrow in the search results to get more details.
		
	RATING FUNCTION
	
	In order to rate a professor, please follow these steps:
		- Make sure you are on the course detail page for the desired course and logged in.
		- Click on the professor name
		- Select your rating for Helpfulness (1-5)
		- Select your rating for Clarity (1-5)
		- Select your rating for Easiness (1-5)
		- Select your rating for Textbook Use (1-5)
		- Click on the rate button. You have just rated a professor.
		
	COMMENT	FUNCTION	
	
	In order to comment on a course, please follow these steps:
		- Make sure you are on the course detail page for the desired course and logged in.
		- Click on the Add Comment button
		- Write your comment in the textbox
		- Click on the Send button. You have now commented on a course

	
	UPVOTE/DOWNVOTE FUNCTION
	
	In order to comment on a course, please follow these steps:
		- Make sure you are on the course detail page for the desired course and logged in.
		- Click on the thumb up or thumb down icons above a comment. Thumb up is an upvote and thumb down is a downvote.

		
	COMMENT DELETION FUNCTION
	
	In order to delete a comment, please follow these steps:
		- Make sure you are logged in
		- Click on your username in the navigation bar
		- Click on the Delete button for the comment you would like to delete

		
	PASSWORD CHANGE
	
	In order to change your password, please follow these steps:
		- Make sure you are logged in
		- Click on your username in the navigation bar
		- click on the Change Password button
		- Enter new password
		- Click on the Submit button. You have just changed your password.

	

	
IMPLEMENTATION DOCUMENTATION

	TECHNOLOGY
	
	The implementation of the course review web application made use of different technologies to achieve the desired 
	functionalities. The technology and tools used in this project are the following:
	
		- Django as the web application framework
		- SQLite for the database
		- Materialize CSS for the front-end
		- Amazon Web Services Elastic Beanstalk as the cloud hosting platform
		- JQuery as the JavaScript library
		- Python, Perl, HTML and CSS as the programming languages
	
	IMPLEMENTATIONS
	
	The choice of Django as the web application framework provided us with a basic structure for the course review web 
	application project. In fact, upon creating a new project with Django, it automatically generates the different files and
	folder structure for the developer.
	
		TEMPLATES
		
		One of the key feature of Django is the possibility of building the front-end upon templates which will reduce the amount
		code to write. Our application makes use different templates to easily generate HTML code for the front-end. These are the
		following:
		
			- base.html: this template is the foundation of all the other templates. it encapsulates the logic for the header, the main 
						content area and the footer. Other templates extends this template.
			- index.html: this template displays user profile information.
			- change_password.html: this template displays the information needed for a password change.
			- login.html: this template displays a form where users provide login information.
			- regist.html: this template displays a form where visitors register to the application.
			- course_list.html: this template displays the list of courses based on the information provided in the search form.
			- course_details.html: this template displays detailed information for each courses such as course name, professors, ratings and comments.
			- new_comment.html: this template displays a form where users can submit comments for a specific course.
			- rating.html: this template allows users to check specific professor's ratings and rate professors.
			- collection.html: this template displays information regarding featured course collection for a specific university.
			- post_edit.html: this template allows the addition of a new course in the database. This template is not in use for this project.
			
			
		VIEWS
		
		Django makes use of views to render the different templates. In addition to template rendering, views encapsulate the logic for each of the template and facilitate the transfer of information between the backend and the template.
		Views are created in "views.py". The different views created in this application are the following:\
		
			- course_list: this view represents the home page. It displays a list of courses from the database.
			- collection: this view obtains featured course collection information.
			- course_detail: this view displays specific course details from the database.
			- agree: this view registers upvotes from the user.
			- disagree: this view registers downvotes from the user.
			- course_new: this view add a new course to the database (not used in this project).
			- comment_new: this view registers new comments from users to the database.
			- rating: this view registers ratings for specific professor to the database.
			- regist: this view registers a new user of the application.
			- login: this view performs the login task for users.
			- index: this view displays users' profiles information from the database.
			- logout: this view performs the logout task for users.
			- change_password: this view performs the password change task for users.
			
		
		MODELS
		
		Django provides a file named "models.py" where developers can create the database for the application. The following are the different tables in our application database:
		
			- course: this table stores courses' information. It has courseid, coursetitle, subject and university as attributes.
			- professor: this table stores professor rating information. It has course (foreign key), full_name, rating, helpfulness, clarity, easiness, textbook and ratetimes as attributes.
			- comment: this table stores users' comments. It has course (foreign key), published_date, user, commenttext, agree, disagree as attributes.
			- account: this table stores users' information. It has username, password, email as attributes.
			- vote: this table stores voting information for each user. It has account (foreign key), prof and courseid as attributes.
			- judge: this tables stores upvotes and downvotes information. It has account (foreign key), user and commentid as attributes.
		
		

	DIFFICULTIES
		
























