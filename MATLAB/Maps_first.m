%Maps
%07/04/2017
map_coords = xlsread('map_coords');
figure
%Last lap
for i = 1:track_points
        velocity_display(i) = v(map_coords(i,1)+1);
end
pointsize = 50;
scatter(map_coords(:,3),map_coords(:,4), pointsize, velocity_display, 'filled')
colorbar
title('Velocity First Lap (m/s)')
xlabel('x')
ylabel('y')
text(-17500,750,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3']);
text(-17500,1500,['Maximum time: ',num2str(max_time),' s']);
text(-17500,2250,['Elapsed time: ',num2str(elapsed_t),' s']);

figure

for i = 1:track_points
        throttle_display(i) = x(map_coords(i,1)+1);
end
pointsize = 50;
scatter(map_coords(:,3),map_coords(:,4), pointsize, throttle_display, 'filled')
colorbar
title('Throttle First Lap (%)')
xlabel('x')
ylabel('y')
text(-17500,750,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3']);
text(-17500,1500,['Maximum time: ',num2str(max_time),' s']);
text(-17500,2250,['Elapsed time: ',num2str(elapsed_t),' s']);


% figure
% 
% for i = 1:1659
%         torque_display(i) = Tm(map_coords(i,1)+1);
% end
% pointsize = 50;
% scatter(map_coords(:,3),map_coords(:,4), pointsize, torque_display, 'filled')
% colorbar
% title('Torque First Lap (Nm)')
% xlabel('x')
% ylabel('y')
% text(-17500,750,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3']);
% text(-17500,1500,['Maximum time: ',num2str(max_time),' s']);
% text(-17500,2250,['Elapsed time: ',num2str(elapsed_t),' s']);
% 

% figure
% 
% plot3(map_coords(:,3),map_coords(:,4),map_coords(:,2),'LineWidth',5)