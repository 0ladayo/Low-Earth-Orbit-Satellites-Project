## Low-Earth-Orbit-Satellites-Project

> In this project, I built a web application that shows the position and altitude of active satellites orbiting the Low Earth Orbit in near real time. The web application also shows the distribution of the count of active low earth orbit satellites vs year of launch and also the proportion of active low earth orbit satellites by purpose.

### Workflow
![a't text](https://github.com/0ladayo/Low-Earth-Orbit-Satellites-Project/blob/master/Workflow.png)

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

> main.py file was deployed to Google App Engine


### Output

>[Low Earth Orbit Satellites Project Web Application](https://leo-satellite-overview-project.nw.r.appspot.com/)

### Blog

> read more here [Building a web application for active low earth orbit satellites](https://medium.com/@Oladayo/building-a-web-application-for-active-low-earth-orbit-satellites-74fcafb16df)

### License

> see the [License](https://github.com/0ladayo/Low-Earth-Orbit-Satellites-Project/blob/master/LICENSE.txt) file for license rights and limitations (MIT)
