%% STEMlab measurements for Bode plots
% @author: Mirco Meiners (HSB)
% Input signal: DF_IN1
% Output signal: DF_IN2
clear;

%% Define Red Pitaya as TCP client object
IP = '192.168.111.183';  % IP of your Red Pitaya ...
port = 5000;
RP = tcpclient(IP, port);
RP.InputBufferSize = 16384*32;

%% Open connection to Red Pitaya
RP.ByteOrder = "big-endian";
configureTerminator(RP, "CR/LF");

flush(RP);

%% Generate continous signal
func = "SINE";  % {sine, square, triangle, sawu, sawd, pwm}
ampl = 0.5;  % Set amplitude
offset = 0.0;  % Set offset
freqs = [500:100:2000];  % Set frequencies


%% Loop to measure multiple tones
for n = 1:length(freqs)
    % Send SCPI command to Red Pitaya to turn ON generator
    writeline(RP,'GEN:RST');  % Reset Generator
    writeline(RP,strcat("SOUR1:FUNC ", func));  % Set function of output signal
    writeline(RP,strcat("SOUR1:VOLT ", num2str(ampl)));  % Set amplitude
    writeline(RP,strcat("SOUR1:VOLT:OFFS ", num2str(offset)));  % Set offset
    writeline(RP,strcat("SOUR1:FREQ:FIX ", num2str(freqs(n))));  % Set frequency
    writeline(RP,'OUTPUT1:STATE ON');  % Turn on output OUT2
    
    writeline(RP,'SOUR1:TRig:INT');  % Generate trigger
    
    pause(1);

    % Trigger
    writeline(RP,'ACQ:RST');  % Input reset
    writeline(RP,'ACQ:DATA:FORMAT ASCII')
    writeline(RP,'ACQ:DATA:UNITS VOLTS')
    writeline(RP,'ACQ:DEC 64');  % Decimation 64
    writeline(RP,'ACQ:TRIG:LEV 0.5');  % Trigger level
    
    % Set trigger delay to 0 samples
    % 0 samples delay sets trigger to the center of the buffer
    % Signal on your graph will have the trigger in the center (symmetrical)
    % Samples from left to the center are samples before trigger
    % Samples from center to the right are samples after trigger
    
    writeline(RP,'ACQ:TRIG:DLY 8192');  % Delay
    writeline(RP,'ACQ:SOUR1:GAIN LV');  % Sets gain to LV/HV (should be the same as jumpers)
    writeline(RP,'ACQ:SOUR2:GAIN LV');  % Sets gain to LV/HV (should be the same as jumpers)
    
    % Start & Trigger
    % Trigger source setting must be after ACQ:START
    % Set trigger to source 1 positive edge

    writeline(RP,'ACQ:START');

    % After acquisition is started some time delay is needed in order to acquire fresh samples in the buffer
    pause(1);
    % Here we have used time delay of one second, but you can calculate the exact value by taking into account buffer
    % length and sampling rate

    writeline(RP,'ACQ:TRIG NOW');  % Instant data aquisition
        
    % Wait for trigger
    % Until trigger is true wait with acquiring
    % Be aware of the while loop if trigger is not achieved
    % Ctrl+C will stop code execution in MATLAB

    while 1
       trig_rsp = writeread(RP,'ACQ:TRIG:STAT?');
       if strcmp('TD',trig_rsp(1:2))  % Read only TD
           break;
       end
    end

    % Read data from buffer
    IN1 = writeread(RP,'ACQ:SOUR1:DATA?');
    IN2 = writeread(RP,'ACQ:SOUR2:DATA?');

    % Convert values to numbers.
    % The first character in string is "{" and the last 3 are 2 spaces and "}".
    
    IN1_num = str2num(IN1(1, 2:length(IN1)-3));
    DF_IN1(:,n) = IN1_num';

    IN2_num = str2num(IN2(1, 2:length(IN2)-3));
    DF_IN2(:,n) = IN2_num';
    
    % Turn off generator OUT1
    writeline(RP,'OUTPUT1:STATE OFF');
end

    
%% Close connection to Red Pitaya
clear RP;


%% Save data as mat file
save('./data/IN_INT.mat', 'DF_IN1', 'DF_IN2');
% save('./data/IN1_INT.mat', 'DF_IN1');
% save('./data/IN2_INT.mat', 'DF_IN2');

%% Save data as parquet file
% parquet data is of type table, no matrix operations
parquetwrite('data/IN1_INT.parquet', array2table(DF_IN1));
parquetwrite('data/IN2_INT.parquet', array2table(DF_IN2));

%% Save data as excel sheet
% data is table data, no matrix operations
% writematrix(DF_IN1, './data/IN1_UB_VBS_mat.xlsx');
% writematrix(DF_IN1, './data/IN2_UB_VBS_mat.xlsx');
% writematrix(DF_IN1, './data/IN_UB_VBS_VBP_mat.xlsx', 'Sheet', 1);
% writematrix(DF_IN2, './data/IN_UB_VBS_VBP_mat.xlsx', 'Sheet', 2);
