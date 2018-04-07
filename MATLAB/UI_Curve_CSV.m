% Set the maximum Current
max_current = 25;

I_s(1) = 0;
I_e(1) = 0;
t_d(1) = 30 * 10^6;
status = 1;

for i = 2:1:100
    if I_s(i-1) < max_current && status
        I_s(i) = I_s(i-1) + 0.5;
        I_e(i) = I_e(i-1) + 0.5;
        t_d(i) = 30 * 10^6;
        
    else
        I_s(i) = 0;
        I_e(i) = 0;
        
        % Minimum sequence time is 10 micro seconds
        t_d(i) = 10;
        
        status = 0;
    end
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