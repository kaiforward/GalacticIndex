# Galactic Index (planetary trade simulation)

## Overview

### What is this site for?

This site is a tool to view data pulled from a planetary trade simulation, involding buying/selling of minerals, and companies trying to profit from the avaiable simulated market

### What does it do?

This site will alow people to view data on invididual planets, their names, climate, amounts of resources and the prices those are bought and sold at, as well as companies, with names, locations, profits and list of trades made

### How does it work

The front end of the site will make extensive use of D3 for data visualisation, the backend will run on python with a MongoDB database

## Features

### Existing Features
- simple planetary simulation, where planets create and use up resources, surplus of resouces will be sellable items, lack of resources will be items they buy.
- any amount of planets can be created and are randomly given the following attributes as well as many others: Name, Habitability, Climate, Resources, Required Resources, Buy/Sell Prices, x,y Locations
- planets now experience crashes, booms and have different populations that affects other variables.
- Companies are also created, with names and locations, At the moment they have the ability to look at the cheapest sell prices and best buy prices and determine the most profitable mineral at the current time.
- UPDATED: Companies can now buy and sell minerals, have expenses and profit levels, these profit levels dictate the stock prices for each company.

### Pages/Features Left to Implement
- All front-end features stil to be decided
- Connecting data with D3 frontend
- Finish Creating Companies so they can make purchases, show profit and that profit is translated into stock prices.
