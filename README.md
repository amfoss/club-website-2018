# **Project**

It’s been 10+ years now that FOSS@Amrita came into existence. We are a community of students supporting and guiding each other towards making open source contributions, which not only helps the members to build technical skills but also helps us to contribute back to the society. Being one of the most active student communities of the country, we have made our presence felt all over. We have been getting a lot of exposure and opportunities via different platforms such as conferences and social media, to name a few. 

**Idea / Goal of the club**: To be a better human being.


## **How to Contribute?**

### If you are a developer:

* Get the code.
* Familiarize yourself with the code base.
* Get familiarised with Git.

1. Bug fixing:
  The first area where you can help is bug fixing. You can look up for the bugs in the ‘issues’. The bugs have been provided with tags to help you classify and work on based on their difficulty level.

2. Feature Development:
  Once you get familiar with the code base, you can start contributing to new features. 


* If you are a designer or usability professional, help shape the UX:

You can contribute in many ways to improve the User Experience of the foss website. Be it reviewing current features as a user and giving feedback, designing new features, testing designs or features with users, we are open for suggestions and, we'd love to have your help in the UX group! 

* If you want to help with the foss website

  1. Providing Website feedback
                 Do provide general feedback about the foss website, to help us improve on the user experience.

  2. Getting Involved In Website Content
                  We welcome participation in creating great content on foss website to help improve projects    and the community. 

* If you're a tester, get started right way!
Start by building the code, and testing all our new exciting features!!

* If you're hoping to contribute in another way, let us know!


## **Getting started**

Getting started with contributing to this is really easy with just one step away from contributing to FOSS@Amrita. So let’s get started:

*   Fork the repository: [https://github.com/amfoss/website]

*   Do a direct clone, so that you can get familiarised with the code base. Moreover a cloned copy on your local system will help you to reproduce bugs and see the changes you make real time.

    git clone [https://github.com/amfoss/fosswebsite.git]


## **Pre-requisites**
1. Install requirements:
  All the requirements are mentioned in the file
   `requirements.txt`

    `pip install -r docs/requirements.txt`

2. Install `python-pip`, `python-dev` and `virtualenvwrapper`

       sudo apt-get install 
       python-pip python-dev
       sudo -H pip install virtualenvwrapper`


## **Installing**
1. First, some initialization steps. Most of this only needs to be done one time. 
Add the command to source:
           `/usr/local/bin/virtualenvwrapper.sh` to your shell startup file
            (`.bashrc` or `.zshrc`) 
            changing the path to `virtualenvwrapper.sh`, depending on where it was installed by `pip`.

       export WORKON_HOME=~/Envs
       mkdir -p $WORKON_HOME
       source /usr/local/bin/virtualenvwrapper.sh`

2. Lets create a virtual environment for our project

       mkvirtualenv --python=which python3 foss
       workon foss

3. Now to set up the database
   In the development phase, we use sqlite3.db
          * Setup tables in the DB

       python manage.py makemigrations

       python manage.py migrate
                
       * Collect all the static files for fast serving
            
       python manage.py collectstatic
       
       * For creating an admin account

       python manage.py createsuperuser'

4. Run server
       
       python manage.py runserver

## **Built with:**

**Frontend**: HTML5, CSS3, JavaScript, jQuery   

**Backend/Framework:** 
* Django 1.11
* Media Query CSS for multi-device compatibility **(Mobile compatibility)**   

**Others:** 
* Google Crawler
* Google Calendar/Google APIs   

**Database:** Django In-built db support (sqlite3)


## **Features implemented:**

**Achievements:**
* **Contributions**: A detailed account of the numerous contributions done by the club members in their respective Open Source organizations. 
* **Articles**: The various informative articles written by our Alumni and students for various Asian and other international magazines are contained in an organised manner
* **GSoC**: A timeline enlisting the details of students selected for GSoC every year with including the  organizations they contribute to and the related projects.
* **RGSoC**: A timeline enlisting the details of students selected for RGSoC every year. 
* **Talks**: Referencing to the talks and conferences given/attended by the students of the club.
* **Internships**: Provides a brief outline of various internship programs enrolled in by the club members.
* **Contests**: Gives out a detailed account of various contests participated and the rank obtained by the members of FOSS@Amrita.   
* **Club Management**
There are various activities in-store to manage and keep up the work-environment. We list them below:
* **Attendance management**: Reflects number of people present during lab working hours and their respective attendance percentage. 
* **Responsibility**: Describes the individual responsibilities assigned to the club members.
* **Teams**: Lists out the teams working on various projects simultaneously.
* **Status updates**: Involvement of a mailing list for sending weekly status updates to keep up with our work and stay updated with current club activities.

**Registration:**   
Social Oauths integrated to do registration and login.
Social Oauth is part of the Social API. It provides a common interface for creating modules related to user registration/login through social networks' accounts.

The student can login and create profile  via a portal but has to be reviewed/verified by a superuser/admin from the admin dashboard.

**Additional pages:**
* User profile
* Sign-Up
* Login
* Password Reset
* Password Change.

**Join Us:**   

Currently, users (members of the club) can contribute to our website via giving their feedback by filling a review application stating their experience with the current system and suggesting the proposed changes, which will help us to improve. For those who are yet to join(first year’s) can fill the Membership Application which in will help us in shortlisting them for the interview round.
* Membership Application
* Review Application

**Projects:**
* Consists of a detailed explanation of various ongoing projects under  a concerned mentor and the mentee(s) contributing to it. (Which includes all personal projects, GSoC projects, Final year projects by FOSS students and much more.) 

**Workshops:**
* Gives a brief account of the workshops conducted by the club for the benefit of all the students as a whole.
* Students who are willing to participate in the workshops conducted could register through the portals being created.

**Documents:**
* Managing important documents: Documents relating to important student information for restricted access by the student and their respective mentors will be catalogued carefully. These include: College specific documents: necessary for obtaining permission to attend conferences and to conduct workshops. Letter templates that would be useful for formal communications, Visa application letters etc.

**Notice Board:**   
This section specifically aims to bridge the procedural/communicational gap between students and administrators, by means of a two-way correspondence between site users and admins. This attribute also serve as a means of sending crucial updates through push notifications or necessary alerts for scheduling important meetings, deadlines (GSoC, Contests) etc.

Basically, any immediate suggestion/improvement is conveyed easily by an admin/mentor to the other members/students through this feature.    

**Events:**
* Info about current and past events conducted by the club. All events can be handled in the same format, the data stored in a db and displayed on the webpage. 

  * Event types: Talks, Workshops, Video Screening (Linux con talks, TED talks etc) 


**Resources**

It consists of all sorts of learning materials, links to different items, which could be accessed from one place.
* Includes a question bank of helpful interview related questions and tasks & online tests for students.
  * Company papers (Microsoft, Google, Amazon)
  * Students sharing their personal interview experiences as blog posts. 
  * Including books such as 
    * How to crack a coding interview;
    * How to move Mount Fuji
* Important Course links from various online learning platforms regarding all domains to benefit students.
* A table representation or Excel sheet db consisting a list of all the GSoC and RSoC proposals selected

**Gallery:**
1. Foss trip pictures
2. Contest/Conference pics
3. Achievement images

**Timeline:**
1. A short para with details on the work they did while they were in the club and a short note about them.
2. An alumni enlisting: Current occupation, areas of expertise photos, resume, blog links.

**Google Analytics**   
Simply put, by far the best way to know our audience, Google Analytics primarily tracks and reports website traffic. Through Analytics, we can monitor how long users stay on our website, what pages/sections they are visiting the most, which page/section is causing the users to leave most often and much more. This would help in substantially improving the performance of the site and improve scalability from the end-user’s perspective.
 
**Social OAuth integration:**
Implementing Social Authentication, users could leverage their existing social network accounts to log in to the site.This would also allow, seamless integration with other features provided by the social network.  

**Chatbot**: Gives the users new ways to interact with our website by engaging in voice and text-based conversational interfaces powered by AI, which would furthermore help the users to ask their prefered doubts and questions regarding our community & work.

**Tools**
1. Artificial Intelligence.
2. [api.ai]

**An Alert Page:** Alert for scheduled meetings, deadlines (GSoC, Contests) etc.   
**Blog Aggregator:** Service that aggregates data using RSS feeds of a blog and displays the latest posts ordered on the website.

## **Contributors**
* Chirath R- Fullstack Developer
* Rahul Krishnan- Backend Developer
* Navaneeth S- Backend Developer
* Chiranjeeb Mahanta-  Backend Developer
* Aniketh Gireesh- Frontend and UI/UX Designer

