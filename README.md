## Low-Earth-Orbit-Satellites-Project

> In this project, I built a web application that shows the position and altitude of active satellites orbiting the Low Earth Orbit in near real time. The web application also shows the distribution of the count of active low earth orbit satellites vs year of launch and also the proportion of active low earth orbit satellites by purpose.

### Languages and Tools Used

#### Pandas

> pandas library was used to access data from the celestrak database, clean and organize the data in a DataFrame structure and stores the dataframe in a google cloud storage bucket.

#### Google Cloud Function

> the data wrangling.py file was deployed as a function in google cloud. 

#### Google Cloud Scheduler

> the google cloud scheduler was used to ensure the google cloud function runs at a specified time. This ensures new satellites data are captured from the celestrack database.

#### Plotly

> plotly library was used for the data visualization

#### Dash

> dash library was used to build the interactive web framework.

#### PyOrbital

> Pyorbital library was used to obtain the latitude, longitude and altitude of the satellites.

#### Google App Engine (GAE)

> google app engine was used to deploy the main.py file


### Output

>[Low Earth Orbit Satellites Project Web Application](https://leo-satellite-overview-project.nw.r.appspot.com/)
