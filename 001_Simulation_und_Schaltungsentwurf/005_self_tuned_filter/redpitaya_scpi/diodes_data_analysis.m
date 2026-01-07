%% Data analysis for Bode plots
% @author: Mirco Meiners (HSB)
% Input signal: DF_IN1
% Output signal: DF_IN2


%% Load data from mat file
% load('./data/IN_D1.mat');
load('./data/IN1_D1.mat');
load('./data/IN2_D1.mat');


%% Load data from parquet file
% parquet data is table data, no matrix operations
% T_IN1 = parquetread('./data/IN1_D1.parquet');
% table to matrix conversion, table2matrix
% DF_IN1 = T_IN1{:,:};
% T_IN2 = parquetread('./data/IN2_D1.parquet');
% table to matrix conversion, table2matrix
% DF_IN2 = T_IN2{:,:};


%% Load data from excel sheet
% DF_IN1 = readmatrix('./data/IN1_D1.mat.xlsx');
% DF_IN2 = readmatrix('./data/IN2_D1.mat.xlsx');
% DF_IN1 = readmatrix('./data/IN_D1.mat.xlsx', 'Sheet', 1);
% DF_IN2 = readmatrix('./data/IN_D1.mat.xlsx', 'Sheet', 2);

%% Darstellung
t = linspace(0, 2.097e-3, 16384)  % Skalierung der Zeitachse
DF_MATH = (DF_IN1(:,1) - DF_IN2(:,1)) / 1e3;

% 1. Achse
yyaxis left
plot(t * 1e3, DF_IN1(:,1))
plot(t * 1e3, DF_IN2(:,1))
xlabel('Zeit t in ms')
ylabel('Spannung in V')

% 2. Achse
yyaxis right
plot(t * 1e3, DF_MATH * 1e6)
ylabel('Strom in $\mu$A')
