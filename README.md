# Galactic Index (planetary trade simulation)

## Overview

### What is this site for?

This site is a tool to view data pulled from a planetary trading simulation, involving buying/selling of minerals, and companies trying to profit from the available simulated market.

### What does it do?

This site will allow people to view data on individual planets, their names, climate, amounts of resources and the prices those are bought and sold at, as well as companies, with names and locations.

### How does it work?

The front end of the site will make extensive use of D3, DC and crossfilter for visualisation of the data, the backend will run on python with a MongoDB database.
The graphs will allow the users to view detailed info on both companies and planets and about what minerals they own/sell. These pages will implement a feature to switch on-page between individual planets data for quick browsing between them. The front page will feature graphs which cover more broad data about the subject and make more use of crossfilter and DC to allow users to see how the different data relates.

## Tech Used

### Some the tech used includes:
- [Bootstrap](http://getbootstrap.com/)
    - I use **Bootstrap** to include some useful layout functionality like tabs.
- [npm](https://www.npmjs.com/)
    - **npm** to help manage some of the dependencies in our application
- [bower](https://bower.io/)
    - **Bower** is used to manage the installation of our libraries and frameworks
- [JQuery](https://jquery.com/)
  - **JQuery** is used for extra front-end functionality.
- [D3](https://d3js.org/)
  - **D3** is used to along with other graphic libraries to visualise the data.
- [Crosffilter](https://github.com/square/crossfilter)
  - **Crossfilter** is used to refine the data for use in our D3 and DC graphs.
 - [DC](https://dc-js.github.io/dc.js/)
  - **DC** is used for extend my graph's functionality and improve user experience.
  
## Contributing

First make sure you have downloaded and installed pycharm, there is a free community edition that works fine for this set-up. 
- [Pycharm](https://www.jetbrains.com/pycharm/)

This project also uses Python version 2.7

  ```
  npm install
 
  bower install
  ```
 
