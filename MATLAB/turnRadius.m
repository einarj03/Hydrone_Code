turn_data = readtable('turn3norm.csv'); %gradient around the track (10 laps)
turn_data = table2array(turn_data); %converted to array

addpath('circfit/');

x = turn_data(:,1);
y = turn_data(:,2);

[R,XC,YC,ERR] = circfit(x,y)