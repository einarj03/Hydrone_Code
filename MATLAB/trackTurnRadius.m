track_data = readtable('track_points.csv'); %gradient around the track (10 laps)
track_data = table2array(track_data); %converted to array

addpath('circfit/');

x = track_data(:,2);
y = track_data(:,3);

r = meancircfit(x,y,30);

disp(['Size of r: ',num2str(size(r,2))]);
while size(r) < 1940
    r(size(r)+1) = 0;
end

for i = 1:1:track_points
    if r(i) > 30
        r(i) = 0;
    end
end

figure
plot(d_1,r)
title('Turning Radius')
xlabel('d (m)')
ylabel('Turning Radius throughout Track')
