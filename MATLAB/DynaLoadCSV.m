% % % Program that turns the power demand into a csv for the dynamic load
%{ ONCE THE FILE IS WRITTEN YOU MUST DO TWO THINGS
% 1) Open excel and highlight all the cells, and re-select General as the
% cell format
% 2) Open the csv file in a text editor and copy and paste the following
% commas to the bottom of the file
,,,,,,,
,,,,,,,
,,,,,,,
%}


% Divide the power demand at the wheels by the motor efficiency
for i = 1:1:total_points
    P_m(i) = P(i) / eff_m(i);
end

k = 1;
i = 1;
while i < total_points
    P_s(k) = P_m(i);
    i_s = i;
    
    condition_1 = (P_m(i) > 0);
    while condition_1
        if i < total_points
            i = i + 1;
            condition_1 = (P_m(i) > 0);
        else
            condition_1 = 0;
        end
    end
    
    P_e(k) = P_m(i-1);
    t_d(k) = str2num(num2str((sum(t(1:i-1)) - sum(t(1:i_s)))*10^6,'%.0f'));
%     Look at time, see which time gap it refers to
%     convert to Current

    k = k + 1;
    
    i_s = i-1;
    
    condition_2 = (P_m(i) == 0);
    while condition_2
        if i < total_points
            i = i + 1;
            condition_2 = (P_m(i) == 0);
        else
            condition_2 = 0;
        end
    end
    
    P_s(k) = 0;
    P_e(k) = 0;
    t_d(k) = str2num(num2str((sum(t(1:i-1)) - sum(t(1:i_s)))*10^6,'%.0f'));
        
    
    k = k + 1;
    
end

% Dynamic load requires 100 rows exactly
% This fills out P_e, P_s and t_d with 0 until there are 100 rows
while k <= 100
    P_s(k) = 0;
    P_e(k) = 0;
    t_d(k) = 0;
    k = k + 1;
end

% Minimum sequence time is 10 micro seconds
for k = 1:1:100
    if t_d(k) == 0
        t_d(k) = 10;
    end
%     t_d(k) = num2str(t_d(k),'%.0f');
end

% % Convert the power values into current values

current_coeff = [3.4556*10^-5 4.1832*10^-2 -5.1399*10^-2];
for k = 1:1:100
    if P_s(k) == 0
        I_s(k) = 0;
    else
        I_s(k) = round(current_coeff(1)*P_s(k)^2 + current_coeff(2)*P_s(k) + current_coeff(3), 2);
    end
    
    
    if P_e(k) == 0
        I_e(k) = 0;
    else
        I_e(k) = round(current_coeff(1)*P_e(k)^2 + current_coeff(2)*P_e(k) + current_coeff(3), 2);
    end
    
    I_s(1) = 0;
end

% % Dynamic load columns:

% Columns 1-5 are all zeros
M_1 = zeros(100,5);

% 6: DC start offset, 7: DC end offset, 8: Sequence point time in ?s, rest are 0
M_2 = [I_s.' I_e.' t_d.'];

M = [M_1 M_2];

fileName = 'WAVE_I.csv';

csvwrite(fileName,M);

% % NOT FINISHED YET
%{ Once the file is written you must do two things
% 1) Open excel and highlight all the cells, and re-select General as the
% cell format
% 2) Open the csv file in a text editor and copy and paste the following
% commas to the bottom of the file
,,,,,,,
,,,,,,,
,,,,,,,
%}




