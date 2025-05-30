<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django." /></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-360/)

![Helli5](http://bayanbox.ir/preview/3500780877665903653/helli5-logo.jpg)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Runnig the Project Locally](#running-the-project-locally)
* [Roadmap](#roadmap)
* [Database structure](#database-structure)
* [Contributers](#contributers)





<!-- ABOUT THE PROJECT -->
## About The Project
This project is a high school website which gives the school boards and teachers
the opportunity to inform students, upload homework and etc.
 






### Built With
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Django](https://www.djangoproject.com)



<!-- GETTING STARTED -->
## Getting started

### Prerequisites
prerequisites packages install with below command
```
$ sudo pip3 install -r requirements.txt 
```
in order to run this project you need to install few packages which its listed below


1)python 3.11
```
$ sudo apt-get update
$ sudo apt-get install python3.11
```
2)pip
```
$ sudo apt install python-pip

```
prerequisites packages install with below command
```
$ sudo pip install -r requirements.txt
```

<!-- Running the Project Locally -->
### Running the Project Locally
First, clone the repository to your local machine:
```
$ git clone https://github.com/mohsen81666/helli5-website.git
```

Add .env file with required data to the project root

Create the database
```
$ python manage.py makemigrations
$ python manage.py migrate [--run-syncdb]
```
Finally, run the development server
```
$ python manage.py runserver
```

<!-- ROADMAP -->
## Roadmap

See the [Network graph](https://github.com/TheMn/internet-engineering-project/network) for timeline of the most recent commits to this repository and its network ordered by most recently pushed to.


<!-- LICENSE -->
## Database structure
* we've used sqlite3 as our db manager which is the django default database.
* below is an Er Diagram of our models and their relations.
 
![Image of Er](http://bayanbox.ir/view/8823936539620629848/db-er.jpg)





<!-- CONTACT -->
## Contributers
* [@mahdi13761376](https://github.com/mahdi13761376) Mahdi Ghanbari - Project Manager
* [@asal97](https://github.com/asal97) Asal Asgari - Database Developer
* [@Emadpourjafar](https://github.com/Emadpourjafar) Emad Pourjafar - Front-End Developer
* [@TheMn](https://github.com/TheMn) Amirhossein Mahdinejad - Back-End Developer

Project Link: [https://github.com/TheMn/internet-engineering-project](https://github.com/TheMn/internet-engineering-project)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TheMn/internet-engineering-project?style=flat-square
[contributors-url]: https://github.com/TheMn/internet-engineering-project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TheMn/internet-engineering-project?style=flat-square
[forks-url]: https://github.com/TheMn/internet-engineering-project/network/members
[stars-shield]: https://img.shields.io/github/stars/TheMn/internet-engineering-project?style=flat-square
[stars-url]: https://github.com/TheMn/internet-engineering-project/stargazers
[issues-shield]: https://img.shields.io/github/issues/TheMn/internet-engineering-project?style=flat-square
[issues-url]: https://github.com/TheMn/internet-engineering-project/issues


