********
### SEM Track Points.xlsx ###
********

contains the longitude, latitude and altitude coordinates of every point along the 2018 track

other sheets calculate the gradient at every point, plot the x-y of the track and also the elevation

********
### map_coords.csv ###
********

contains the longitude and latitude coordinates of every point along the 2018 track

this must be updated every year to fit the new track

********
### theta_e.csv ###
********

contains the gradient at every point along the track

********
### Strategy2018v4.m ###
********

run this program to model the vehicle's performance around the track

see how changing certain parameters such as weight, rolling resistance, aero-drag, fuel cell efficiency, power electronic efficieny, etc. affect the final efficiency value

other things that can be changed include locations along the track that require speed limits, motor characteristics, vehicle characteristics, etc.

this program requires an up-to-date theta_e.csv file

********
### DynaLoadCSV.m ###
********

the Strategy program must be run before this program can be run

this program calculates the equivalent electrical load that the motor controller would demand throughout the race

this can be used to simulate the vehicle's performance in the competition

note that for this program to work you must use the correct conversion from power to electrical power (depending on if there is a DC-DC converter operating at 48V or whether the fuel cell is being run stright, or any other configuration)

********
### Maps.m ###
********

the Strategy program must be run before this program can be run

this program plots the velocity and throttle needed at every point along the track, it is good for visualising where velocity is higher, and where throttle must be applied

********
### trackTurnRadius.m ###
********

this program plots the approximate turning radius everywhere along the track