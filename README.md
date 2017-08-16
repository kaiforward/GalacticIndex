# Galactic Index (planetary trade simulation)

## Overview

### What is this site for?

This site is a tool to view data pulled from a planetary trade simulation, involving buying/selling of minerals, and companies trying to profit from the available simulated market

### What does it do?

This site will allow people to view data on individual planets, their names, climate, amounts of resources and the prices those are bought and sold at, as well as companies, with names, locations, profits and list of trades made

### How does it work

The front end of the site will make extensive use of D3 for data visualisation, the backend will run on python with a MongoDB database

## Features

### Existing Features
- Simple planetary simulation, where planets create and use up resources, surplus of resouces will be sellable items, lack of resources will be items they buy.
- Any amount of planets can be created and are randomly given the following attributes as well as many others: Name, Habitability, Climate, Resources, Required Resources, Buy/Sell Prices, x,y Locations
- Random Name generator creates all planet, elements and company names. Uses Old Norse for fun.
- UPDATED: Planets now experience crashes, booms and have different populations that affects other variables.
- UPDATED: Companies are now created, with names and locations, At the moment they have the ability to look at the cheapest sell prices and best buy prices and determine the most profitable mineral at the current time.
- UPDATED: Companies can now buy and sell minerals, have expenses and profit levels, these profit levels dictate the stock prices for each company.
- UPDATED: Companies now have have an amount of ships and spaceports, which limit their trade, if they earn enough they will buy more spaceports for more ships.

### Pages/Features Left to Implement
- All front-end features still to be decided
- Connecting data with D3 frontend
- Creating Companies
- Finish Creating Companies so they can make purchases, show profit and that profit is translated into stock prices.
