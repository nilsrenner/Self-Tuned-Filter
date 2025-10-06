%% Data analysis for Bode plots
% @author: Mirco Meiners (HSB)
% Input signal: DF_IN1
% Output signal: DF_IN2
clear

%% Array of tones (GEN), input signal
ampl = 0.5;
offset = 0.0;
freqs = [100:5:250];  % Set frequencies
w = 2*pi*freqs;
t = linspace(0, 8.389e-3, 16384);
ts = 8.389e-3/16384;  % sampling time

%% Load data from mat file
load('./data/IN_INT.mat');
% load('./data/IN1_INT.mat');
% load('./data/IN2_INT.mat');

%% Load data from parquet file
% parquet data is table data, no matrix operations
T_IN1 = parquetread('./data/IN1_INT.parquet');
% table to matrix conversion, table2matrix
DF_IN1 = T_IN1{:,:};
T_IN2 = parquetread('./data/IN2_INT.parquet');
% table to matrix conversion, table2matrix
DF_IN2 = T_IN2{:,:};


%% Load data from excel sheet
% DF_IN1 = readmatrix('./data/IN1_UB_VBS.xlsx');
% DF_IN2 = readmatrix('./data/IN2_UB_VBP.xlsx');
% DF_IN1 = readmatrix('./data/IN_UB_VBS_VBP.xlsx', 'Sheet', 1);
% DF_IN2 = readmatrix('./data/IN_UB_VBS_VBP.xlsx', 'Sheet', 2);


%% Fitting and extraction of sine params

for n = 1:length(freqs)
    SigParam_IN1(:,n) = fit_sin(t, DF_IN1(:,n)');
    SigParam_IN2(:,n) = fit_sin(t, DF_IN2(:,n)');
end
    

%% Amplitudes via std
% MAG_dB = 20*log10(std(DF_IN1) ./ ampl);
MAG_dB = 20*log10(std(DF_IN2) ./ std(DF_IN1));


%% Phase difference test signal
% Ref.:
% https://stackoverflow.com/questions/27545171/identifying-phase-shift-between-signals
% y1 = ampl * sin(w(1)*t);  % input signal
% dt = 0.2e-3;
% y2 = ampl * sin(w(1)*t - w(1)*dt);  % output sinal


%% Cross-correlation test
%   [C, lag] = xcorr(y1, y2);
%    [maxC, I] = max(C);
%    phase_rad_xcorr = (lag(I) * ts * w(1));
%    phase_deg_xcorr = rad2deg(phase_rad_xcorr);


%% Cross-correlation with dataframes
for n = 1:length(freqs)
    [C, lag] = xcorr(DF_IN1(:,n)', DF_IN2(:,n)');
    [maxC, I] = max(C);
    phase_rad_xcorr(n) = (lag(I) * ts * w(n));
    phase_deg_xcorr = rad2deg(phase_rad_xcorr);
end


%% Frequency domain test
% y1_fft = fft(y1);
% y2_fft = fft(y2);
% phase_rad_fft = angle(y2_fft(1:end/2)/y1_fft(1:end/2));
% phase_deg_fft = rad2deg(phase_rad_fft);


%% Hilbert transform test
% y1_h = hilbert(y1);
% y2_h = hilbert(y2);

% phase_rad_h = angle(y2_h/y1_h);
% phase_deg_h = rad2deg(phase_rad_h);
% phase_rad_h = wrap(angle(y1_h) - angle(y2_h));


%% Hilbert transform with dataframe

for n = 1:length(freqs)
    y1_h = hilbert(DF_IN1(:,n)');
    y2_h = hilbert(DF_IN2(:,n)');

    phase_rad_h(n) = angle(y2_h/y1_h);
    phase_deg_h = rad2deg(phase_rad_h);
end

%% Bode plot
% magnitude
figure(1);
subplot(2,1,1)
plot(freqs, MAG_dB, '.');
grid;
ylabel('Magnitude in dB');
% phase
subplot(2,1,2)
plot(freqs, phase_deg_xcorr, '.');
grid;
xlabel('Frequency in Hz');
ylabel('Phase in deg');
