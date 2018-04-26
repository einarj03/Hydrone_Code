%Optimisation of Driving Stategy
%Jason Biddlecombe
%08/12/2016
clear
clc

%Consumption Target (3rd) = 700 km/m^3

%2017 Track
track_length = 940.512; %m 
no_laps = 15;
total_length = track_length * no_laps; %m
max_time = 35*60; % mins*(seconds/mins) safety factor from 39 mins
lap_time = max_time/no_laps; %s
average_v = track_length/lap_time;
cr = 0.0050; %rolling resistance (safety factor to 0.004)
g = 9.81; %m/s^2
mass_car = 45; %kg 
mass_driver = 50; %kg
m = mass_car + mass_driver; %kg
p_air = 1.225; %kg/m^3 air density
Af = 0.39; %m^2 Frontal area
cd = 0.12; %drag coefficient (safety factor to 0.08)
theta = readtable('theta_e.txt'); %gradient around the track (10 laps)
theta = table2array(theta); %converted to array
% a = zeros(track_length,1);

%%
max_n = 4013; %rpm
min_n = 3295; %rpm
max_T = 1.711; %Nm 
min_T = 0.038; %Nm
G = 5; %input speed / output speed

%Efficiency of motor coefficients
motor_coeff = [-1.89559261 25.04722276 -129.6267401 333.2213722 -447.3435524 ...
294.3967411 16.38573456 ];
   
%%
g_line = (max_T-min_T)/(min_n-max_n);
c = min_T - g_line * max_n;

for n_motor = 1:1:(min_n-1)
    T_motor(n_motor) = max_T;
end

for n_motor = min_n:1:max_n
    T_motor(n_motor) = g_line * n_motor + c ; %Nm
end

%Throttle inclusion
T_motor = T_motor;
%%

n_motor = [1:1:max_n];

T_wheel = T_motor*G; %Nm Torque delivered by the wheel
T_wheel10 = T_wheel; %Default
n_wheel = n_motor/G; %rpm rotational speed of the wheel
r_wheel = 0.239; %m radius of wheel
v_wheel = n_wheel*(2*pi/60) * r_wheel; %m/s speed of the wheel
P_wheel = T_wheel .* n_wheel * (2*pi/60); %W power delivered to the wheel
v_wheel_counter = v_wheel(2)-v_wheel(1); %Velocity steps for power level calulation
v_limit = max(v_wheel);
%Initial conditions for iteration
s = 0.4848;%m Resolution. %1m, 0.1m, 0.01m (or less x 0.1)
track_points = int16(track_length/s);
total_points = int16(total_length/s);
v = zeros(1, total_points);
v(1) = 0.0001;
status = 0;
brake_a = -1; %m/s^2
limit_1 = 7; %m/s
limit_2 = 7; %m/s
limit_3 = 8; %m/s

%%

for q = 1:(total_points)
    if mod(q, track_points) == 0
        i = track_points;
    else
        i = int16(mod(q, track_points));
    end
    
    theta_2(q) = theta(i);
        
end

for i = 1:1:(total_points) %1659 = 1658m (last calculation) as starts at 1 (0m)
  
  Fd(i) = m*g*cr*cos(theta_2(i)) + 0.5*p_air*cd*Af*v(i)^2 + ...
                    m*g*sin(theta_2(i));
                
  k = floor((i-1)/(track_points)); %k = individual lap counter from 1 - 1659 each lap
  k = i - k*(track_points); %Corresponding to 0 - 1658m 
  
  if k == 97 && v(i) > limit_1
    b(i) = limit_1;
    p = i;
        while b(i) < v(i)
        P(i-1) = 0;    
        Fp(i-1) = 0;
        a(i-1) = brake_a;
        b(i-1) = sqrt(b(i)^2 - 2*a(i-1)*s);
        i = i-1;
        end
        
        for j = i:1:p
        v(j) = b(j);
        end
        
        i=j;
             
  end
    
    if k == 992 & v(i) > limit_2
    b(i) = limit_2;
    p = i;
        while b(i) < v(i)
        P(i-1) = 0;    
        Fp(i-1) = 0;
        a(i-1) = brake_a;
        b(i-1) = sqrt(b(i)^2 - 2*a(i-1)*s);
        i = i-1;
        end
        
        for j = i:1:p
        v(j) = b(j);
        end
        
        i=j;
             
    end
    
    if k == 1240 & v(i) > limit_3
    b(i) = limit_3;
    p = i;
        while b(i) < v(i)
        P(i-1) = 0;    
        Fp(i-1) = 0;
        a(i-1) = brake_a;
        b(i-1) = sqrt(b(i)^2 - 2*a(i-1)*s);
        i = i-1;
        end
        
        for j = i:1:p
        v(j) = b(j);
        end
        
        i=j;
             
    end
 
 
    
%%   
% %Strategy
% pc1 = 1;
% cv1 = (700/s);
% pc2 = (750/s);
% cv2 = (1392/s);
% pc3 = (1450/s);
% %Pulse and coast regions
% if (k >= pc1 & k < cv2) | (k >= pc3 & k <= (1659/s))
% if (k >= pc1 & k < cv1) | (k >= pc2 & k <= cv2)| ...
%    (k >= pc3 & k <= (1659/s)) 

%Throttle
T_wheel = T_wheel10*0.8;
% % %     if i < (100/s) %First lap 
% % %     T_wheel = T_wheel10*0.5;
% % %     elseif i >= (100/s) & i < (700/s)
% % %     T_wheel = T_wheel10*0;
% % %     elseif i >= (750/s) & i < (800/s)
% % %     T_wheel = T_wheel10*0.7;
% % %     elseif i >= (800/s) & i < (1200/s)
% % %     T_wheel = T_wheel10*0;
% % %     elseif i >= (1200/s) & i < (1450/s)
% % %     T_wheel = T_wheel10*0.5;
% % %     elseif i >= (1450/s) & i <= (1659/s)
% % %     T_wheel = T_wheel10*0;    
% % %     elseif k < (100/s) & i > (1659/s) %Subsequent laps
% % %     T_wheel = T_wheel10*0;
% % %     elseif k >= (100/s) & k < (175/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0.32;
% % %     elseif k >= (175/s) & k < (750/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0;
% % %     elseif k >= (750/s) & k < (800/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0.6; 
% % %     elseif k >= (800/s) & k < (1000/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0;
% % %     elseif k >= (1250/s) & k < (1450/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0.75;
% % %     elseif k >= (1450/s) & i > (1659/s)
% % %     T_wheel = T_wheel10*0;    
% % %     end
    
%Speed envelope
max_speed = 8.5;
min_speed = 6;
% % %     if i < (100/s) % First lap
% % %     max_speed = 9;
% % %     min_speed = 7;
% % %     elseif i >= (100/s) & i < (700/s)
% % %     max_speed = 9;
% % %     min_speed = 7;
% % %     elseif i >= (700/s) & i < (750/s)
% % %     max_speed = 10;
% % %     min_speed = 7;
% % %     elseif i >= (750/s) & i < (1560/s)
% % %     max_speed = 11;
% % %     min_speed = 7;
% % %     elseif i >= (1560/s) & i <= (1659/s)
% % %     max_speed = 9;
% % %     min_speed = 7; 
% % %     elseif k < (100/s) & i > (1659/s) %Subsequent laps
% % %     max_speed = 9;
% % %     min_speed = 7;
% % %     elseif k >= (100/s) & k < (700/s) & i > (1659/s)
% % %     max_speed = 9;
% % %     min_speed = 7;
% % %     elseif k >= (700/s) & k < (1560/s) & i > (1659/s)
% % %     max_speed = 10;
% % %     min_speed = 7;
% % %     elseif k >= (1560/s) & i > (1659/s)
% % %     max_speed = 9;
% % %     min_speed = 7;   
% % %     end
%Pulse and Coast logic
    if v(i) <= 0 
       break 
    end
        
    if v(i) >= max_speed
        Fp(i) = 0;
        status = 0;
    
%     elseif Fd(i) <= 0 %Coast
%     Fp(i) = 0;
   
    elseif  v(i) <= min_speed %Accelerate as below min
        if v(i)/v_wheel_counter > max_n
            Fp(i) = 0;
        else
            Fp(i) = T_wheel(ceil(v(i)/v_wheel_counter))/r_wheel;%Power corresponding to velocity level
            throttle(i) = T_wheel(1)/T_wheel10(1); %Throttle
        end
        % 0 Force delivered above max speed as rachet system prevents
        % delivery of torque
    status = 1;
       
    elseif  v(i) <= max_speed & v(i) > min_speed & status == 1 %accelerate up to 10
         if v(i)/v_wheel_counter > max_n
         Fp(i) = 0;
         else
         Fp(i) = T_wheel(ceil(v(i)/v_wheel_counter))/r_wheel;%Power corresponding to velocity level 
         throttle(i) = T_wheel(1)/T_wheel10(1); %Throttle
         end
         
    elseif  v(i) <= max_speed & v(i) > min_speed & status == 0 %Coast after max reached
    Fp(i) = 0;
       
    end

%%    
%Efficiency and dynamic calculations
    Tm(i) = (Fp(i)*r_wheel/G); 
   
    eff_m(i) = 0.01 * (motor_coeff(1)*Tm(i)^6 + motor_coeff(2)*Tm(i)^5 + motor_coeff(3)*Tm(i)^4+ motor_coeff(4)*Tm(i)^3 + ...
               motor_coeff(5)*Tm(i)^2 + motor_coeff(6)*Tm(i) + motor_coeff(7));

    P(i) = Fp(i)*v(i);
    a(i) = (Fp(i) - Fd(i))/m;
    v(i+1) = sqrt(2*a(i)*s + v(i)^2);
    
    if isreal(v(i+1)) == 0;
        disp('Complex error3 Less than 0 m/s')
        break
    end
    %Include complex  check - less than 0 m/s
    state(i) = status;
          
end

%%

if v(i) <= 0
    disp('Less than 0 m/s')
end

%Energy consumption converted to hydrogen
%v ends up wih 16591 as v+1 term calculated
v((total_points)+ 1) = [];

% eff_h_coeff_a = [2.6846*10^-10 -9.4316*10^-8 1.2805*10^-5 -8.6395*10^-4 3.0968*10^-2 9.5306*10^-4];

eff_h_coeff_b = [-2.4207*10^-4 0.55413];

for i = 1:1:total_points
    if P(i) < 99
        eff_h(i) = 0.35;
    else
        eff_h(i) = eff_h_coeff_b(1)*P(i) + eff_h_coeff_b(2);
    end
end

eff_c = 0.80;

LCV_H = 120000; %kJ/kg
p_H = 0.089949; %kg/m^3

nominal_flow = 0.108; % in l/min
nominal_P_H = (nominal_flow / (1000 * 60)) * p_H * LCV_H * 1000;

E_H = zeros(1, (total_points - 1));

%add dynamic eff calcs in here  - dependent upon speed.

for i = 1:1:total_points
    P_FC(i) = P(i) / (eff_m(i) * eff_c);
end

for i = 1:1:((total_points)-1) %t and E_H consumed between points (i and i+1)

    t(i) = 2*s/(v(i+1) + v(i));
    
    if P(i) == 0
        E_H(i) =  nominal_P_H * t(i);
    else
        E_H(i) = P(i)*t(i)/(eff_h(i)*eff_c*eff_m(i));
    end
    
end

for i = 1:1:total_points
    P_H(i) = P(i)/ (eff_h(i)*eff_c*eff_m(i) );
    if P_H(i) == 0
        P_H(i) =  nominal_P_H;
    end
end    

%%

E_H_total = sum(E_H);
elapsed_t = sum(t);
d = [0:1:(total_points)-1]; %Actual distances at which there is an input to the car (i.e not total_length)

Fuel_eff = (LCV_H*p_H*total_length*0.001)/(E_H_total*0.001); %km/m^3
Fuel_cons = (E_H_total*0.001) / (LCV_H*p_H*0.001); % l

for i = 1:1:total_points-1
    Fuel_flow(i) = ((E_H(i)*0.001)*60) / ((LCV_H*p_H*0.001)*t(i)); % l/min
end

total_fuel = 80; %l
Fuel_consumption_total = Fuel_cons / total_fuel * 100; % percent

p_G = 764.6; %kg/m^3
NCV_G = 42900; %kJ/kg 
Fuel_eff_gasoline = Fuel_eff*NCV_G*p_G/(p_H*LCV_H*1000); %km/l

base_eff = 552.869;
Eff_Impr = 100*(Fuel_eff - base_eff)/Fuel_eff;

for i = 1:1:total_points
    P_FC(i) = P(i) / (eff_m(i)*eff_c);
end

max_P_m = max(P_FC);

disp(['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3']);
disp(['Elapsed time: ',num2str(elapsed_t),' s']);
disp(['Maximum time: ',num2str(max_time),' s']);
disp(['Efficiency increase: ',num2str(Eff_Impr),' %']);
disp(['Fuel Consumption1: ',num2str(Fuel_cons),' l']);
disp(['Total fuel consumption: ',num2str(Fuel_consumption_total),' %']);
disp(['Max Power at Fuel Cell: ',num2str(max_P_m),' W']);


if v(i) <= 0 
    disp('Less than 0 m/s')
end

if elapsed_t > max_time
    overrun = elapsed_t - max_time;
    disp(['Time exceeded by ',num2str(overrun),' seconds']);
end


%%
%Plot the results
throttle(total_points) = 0; %For plotting purposes (arrays of same length)
t_c = [0,cumsum(t)];

elevation = readtable('elevation.txt'); %m Single lap
elevation = table2array(elevation); %m

for q = 1:(track_points)
    elevation_1(q) = elevation(q);
end

for q = 1:(total_points)
    if mod(q, track_points) == 0
        i = track_points;
    else
        i = int16(mod(q, track_points));
    end
    
    elevation_2(q) = elevation(i);
        
end

%First lap plot data
t_1 = t(1:(track_points-1)); 
t_c_1 = [0,cumsum(t_1)];
v_1 = v(1:(track_points));
P_1 = P(1:(track_points));
Fd_1 = Fd(1:(track_points)); 
Fp_1 = Fp(1:(track_points));
theta_1 = theta_2(1:(track_points));
%Last lap plot data
t_2 = t((total_points)-(track_points)+1:(total_points)-1);
t_c_2 = [0,cumsum(t_2)];
v_2 = v((total_points)-(track_points)+1:(total_points));
P_2 = P((total_points)-(track_points)+1:(total_points));
P_H_2 = P_H((total_points)-(track_points)+1:(total_points));
Fd_2 = Fd((total_points)-(track_points)+1:(total_points));
Fp_2 = Fp((total_points)-(track_points)+1:(total_points));

v_2 = v_2;
v_1 = v_1;
v = v;

d_1 = d(1:track_points)*s;
a_1 = a(1:track_points);

% % Calculating braking forces
for i = 1:1:total_length
    if a(i) == -1
        Fb(i) = m * a(i);
    else
        Fb(i) = 0;
    end
end
Fb_1 = Fb(1:track_points);

% 
% % %Whole race
% % 
% % subplot(2,2,1)
% % plot(t_c,v)
% % title('Velocity')
% % xlabel('Time (s)')
% % ylabel('Velocity (m/s)')
% % text(50,2,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% % text(50,2.5,['Maximum time: ',num2str(max_time),' s']);
% % text(50,3,['Elapsed time: ',num2str(elapsed_t),' s']);
% % 
% % 
% % subplot(2,2,2)
% % plot(t_c,P)
% % title('Power')
% % xlabel('Time (s)')
% % ylabel('Power (W)')
% % 
% % subplot(2,2,3)
% % plot(t_c,elevation_2)
% % title('Elevation') 
% % xlabel('Time (s)')
% % ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(t_c,Fd,t_c,Fp)
% % title('Resistive and Propulsive Force')
% % xlabel('Time (s)')
% % ylabel('Forces acting on the car (N)')
% % 
% % % %Whole race
% % figure 
% % subplot(2,2,1)
% % plot(d,v)
% % title('Velocity')
% % xlabel('d (m)')
% % ylabel('Velocity (m/s)')
% % text(400,2,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% % text(400,2.5,['Maximum time: ',num2str(max_time),' s']);
% % text(400,3,['Elapsed time: ',num2str(elapsed_t),' s']);
% % 
% % 
% % subplot(2,2,2)
% % plot(d,P)
% % title('Power')
% % xlabel('d (m)')
% % ylabel('Power (W)')
% % 
% % subplot(2,2,3)
% % plot(d,elevation_2)
% % title('Elevation') 
% % xlabel('d (m)')
% % ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(d,Fd,d,Fp)
% % title('Resistive and Propulsive Force')
% % xlabel('d (m)')
% % ylabel('Forces acting on the car (N)')
% 
% % % Motor data
% % 
% % subplot(2,2,1)
% % plot(n_motor,T_motor)
% % title('Motor')
% % xlabel('rpm')
% % ylabel('Nm')
% % 
% % subplot(2,2,2)
% % plot(n_wheel,T_wheel10)
% % title('Wheel')
% % xlabel('rpm')
% % ylabel('Nm')
% % 
% % subplot(2,2,3)
% % plot(n_wheel,v_wheel)
% % title('Velocity') 
% % xlabel('Wheel speed (rpm)')
% % ylabel('Wheel speed (m/s)')
% % 
% % subplot(2,2,4)
% % plot(v_wheel,P_wheel)
% % title('Power') 
% % xlabel('Wheel speed (m/s)')
% % ylabel('Wheel Power (W)')
% % 
% % %1st lap
% % 
% % figure
% % subplot(2,2,1)
% % plot(t_c_1,v_1)
% % title('Velocity')
% % xlabel('Time (s)')
% % ylabel('Velocity (kph)')
% % text(50,5,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% % text(50,10,['Maximum time: ',num2str(max_time),' s']);
% % text(50,15,['Elapsed time: ',num2str(elapsed_t),' s']);
% % 
% % 
% % subplot(2,2,2)
% % plot(t_c_1,P_1)
% % title('Power')
% % xlabel('Time (s)')
% % ylabel('Power (W)')
% % 
% % subplot(2,2,3)
% % plot(t_c_1,elevation_1)
% % title('Elevation') 
% % xlabel('Time (s)')
% % ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(t_c_1,Fd_1,t_c_1,Fp_1)
% % title('Resistive and Propulsive Force')
% % xlabel('Time (s)')
% % ylabel('Forces acting on the car (N)')

figure
subplot(2,2,1)
plot(d_1,v_1)
title('Velocity')
xlabel('Distance (m)')
ylabel('Velocity (m/s)')
text(50,5,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
text(50,10,['Maximum time: ',num2str(max_time),' s']);
text(50,15,['Elapsed time: ',num2str(elapsed_t),' s']);


subplot(2,2,2)
plot(d_1,P_1)
title('Power')
xlabel('Distance (m)')
ylabel('Power (W)')

subplot(2,2,3)
plot(d_1,elevation_1)
title('Elevation') 
xlabel('Distance (m)')
ylabel('Elevation (m)')

subplot(2,2,4)
plot(d_1,Fd_1,d_1,Fp_1)
title('Resistive and Propulsive Force')
xlabel('Distance (m)')
ylabel('Forces acting on the car (N)')

% % 
% % 
% % figure
% % subplot(2,2,1)
% % plot(d_1,v_1)
% % title('Velocity')
% % xlabel('Time (s)')
% % ylabel('Velocity (m/s)')
% % text(50,5,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% % text(50,10,['Maximum time: ',num2str(max_time),' s']);
% % text(50,15,['Elapsed time: ',num2str(elapsed_t),' s']);
% % 
% % 
% % subplot(2,2,2)
% % plot(d_1,P_1)
% % title('Power')
% % xlabel('d (m)')
% % ylabel('Power (W)')
% % 
% % subplot(2,2,3)
% % plot(d_1,elevation_1)
% % title('Elevation') 
% % xlabel('d (m)')
% % ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(d_1,Fd_1,d_1,Fp_1)
% % title('Resistive and Propulsive Force')
% % xlabel('d (m)')
% % ylabel('Forces acting on the car (N)')
% 
% % %Last lap
% % 
% figure
% subplot(2,2,1)
% plot(t_c_2,v_2)
% title('Velocity')
% xlabel('Time (s)')
% ylabel('Velocity (kph)')
% text(100,35,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% text(100,37,['Maximum time: ',num2str(max_time),' s']);
% text(100,39,['Elapsed time: ',num2str(elapsed_t),' s']);
% % 
% % subplot(2,2,2)
% % plot(t_c_2,P_2)
% % title('Power at wheels')
% % xlabel('Time (s)')
% % ylabel('Power at wheels (W)')
% % 
% % subplot(2,2,3)
% % plot(t_c_2,elevation_1)
% % title('Elevation') 
% % xlabel('Time (s)')
% % ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(t_c_2,Fd_2,t_c_2,Fp_2)
% % title('Resistive and Propulsive Force')
% % xlabel('Time (s)')
% % ylabel('Forces acting on the car (N)')
% % % 
% % % 
% % %Last lap
% % % 
% % 
% % 
% figure
% 
% subplot(2,2,1)
% plot(d_1,v_2)
% title('Velocity')
% xlabel('d (m)')
% ylabel('Velocity (m/s)')
% text(400,5,['Fuel efficiency: ',num2str(Fuel_eff),' km/m^3'])
% text(400,10,['Maximum time: ',num2str(max_time),' s']);
% text(400,15,['Elapsed time: ',num2str(elapsed_t),' s']);
% 
% subplot(2,2,2)
% plot(d_1,P_2)
% title('Power at wheels')
% xlabel('d (m)')
% ylabel('Power at wheels (W)')
% 
% subplot(2,2,3)
% plot(d_1,elevation_1)
% title('Elevation') 
% xlabel('d (m)')
% ylabel('Elevation (m)')
% % 
% % subplot(2,2,4)
% % plot(d_1,Fd_2,d_1,Fp_2)
% % title('Resistive and Propulsive Force')
% % xlabel('d (m)')
% % ylabel('Forces acting on the car (N)')
% 
% % Braking Forces
% figure
% plot(d_1,Fb_1)
% title('Braking Force around Track')
% xlabel('d (m)')
% ylabel('Braking Force at Wheels (N)')

figure
plot(d_1,Fd_2,d_1,Fp_2,d_1,Fb_1)
title('Resistive and Propulsive Force')
xlabel('d (m)')
ylabel('Forces acting on the car (N)')
% 
% % % % 
% % 
% % hill_total = 0;
% % for i = 16000:1:16589
% %     hill = E_H(i)*eff_m(i)*eff_h;
% %     hill_total = hill_total + hill;
% % end
% 
% figure
% plot(d,P_FC)
% title('Fuel Cell Power Demand Along Track')
% xlabel('d (m)')
% ylabel('Power Demand from Fuel Cell (W)')

% figure
% plot(d(1:total_points-1),Fuel_flow)
% title('Fuel Flow Along Track')
% xlabel('d (m)')
% ylabel('Fuel Flow (l/min)')

% % Motor efficiency
% figure
% plot((min_T:0.01:max_T)

for i = 1:1:total_points
    RPM(i) = v(i) / (2 * pi * r_wheel) * 60;
    Wheel_T(i) = 60 * P(i) / (2 * pi* RPM(i));
end

% Find velocity of i
% Calculate RPM from velocity
% Calculate torque from RPM and P at wheels
    
    
    


