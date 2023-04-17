# CookieAMS
<div id="technologies" style="margin-bottom: 16px;">
  <span>
    <a href="https://www.python.org">
      <img src="https://img.shields.io/badge/-python-3776ab?style=for-the-badge&logo=python&logoColor=white"/>
    </a>
    <a href="https://www.python.org">
      <img src="https://img.shields.io/badge/-pandas-purple?style=for-the-badge&logo=pandas"/>
    </a>
    <a href="https://www.djangoproject.com">
      <img src="https://img.shields.io/badge/-django-darkgreen?style=for-the-badge&logo=django" />
    </a>
    <a>
      <img src="https://img.shields.io/badge/-plotly%20dash-black?style=for-the-badge&logo=plotly"/>
    </a>
    <a>
      <img src="https://img.shields.io/badge/-flask-grey?style=for-the-badge&logo=flask"/>
    </a>
    <a>
      <img src="https://img.shields.io/badge/-sqlite-blue?style=for-the-badge&logo=sqlite"/>
    </a>
    <a>
      <img src="https://img.shields.io/badge/-postgresql-19376D?style=for-the-badge&logo=postgresql&logoColor=white"/>
    </a>
    <a>
      <img src="https://img.shields.io/badge/-Scikit_learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white" />
    </a>
  </span>
</div>

An analytics-based asset management system design to log, monitor, and manage a network of electrical transformers & transformer failures. 

This repository contains the proof-of-concept version of CookieAMS, developed to be presented at the MISSA ITC conference. For more information, [visit their website here](https://www.calpolymissa.org/html/itc.html) 

## Getting Started
1. Create a virtual environment:
```bash
$ virtualenv env
```
2. Activate the virtual environment:
```bash
$ source env/scripts/activate
```
3. Download the required libraries on your virtual environment:
```bash
$ pip install -r requirements.txt
```
4. Run the servers:
```bash
$ ./start.sh api  # Start the API server
$ ./start.sh client  # Start the client server
```

## Features
- #### Table log of all previous transformer failures, along with their specifications
  - Sorting, filtering, and pagination features for tables to enhance user experience.
- #### User-friendly form for logging new transformer failures
  - Built-in authentication protects transformer database from being tampered by unauthorized individuals.
- #### Analytics insight page on various statistics for previous transformer failures
  - Analytics-based predictions using various classification & clustering machine learning models

