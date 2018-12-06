# Project Title
    Web Coding Challenge
        * a Web application for Listing all nearby Stores to a particular user.
        * the user can add the store to favorite list by liking it.
        * the user can dislike the store so the store will be disable for next 2 hours.
        * The user can remove the store from the favorite list.

        * The approach was using 2 models that represent the user and the store and some relation between them since a user is related to the stores that are nears him, for that you need to login or register in order to views your Stores and manipulate them.

## Getting Started
    * To Start the app just get a copy from https://github.com/ninjaEater/store_app.git repository
    ex : git clone https://github.com/ninjaEater/store_app.git
    or you can fork it if you want to collaborate and add some features in the future.

### Prerequisites and Installations
    * You need to install thoses in order to run the app :
        * the latest version of django.
            you can do that by using python package manager pip.
                ```
                - pip install django
                ```
        * you need a library called geocoder this allows you to get information about the user, especially the location of the user based on there ip address.
                - pip install geocoder
        * and also requests module for sending HTTP GET requests to search the stores (based on your latitude and longtitude) to retrieve all stores that are nears you.
                - pip install requests
        * all this stuff could be gather into one single Docker image that contains all requirements files that needed in order to run this app (I will add it as soon as possible) 
## Author
    * Name : RZOUKI ismail
    * Email : ismailrzouki7@gmail.com
    * Github : https://github.com/ninjaEater
    * Tel : 0637505624

## PS's
    * I didn't focus on front end (I used some bootstrap).
    * I used username field instead of Email field, i will upgrade this soon.
    * you can use this to login if you are lazy (register your own to see the stores that nearby your location).
        - username : kosmos
        - password : santoryo1234   
    * I didn't implements any tests for now (this will be in the future so we can use some CI tools).