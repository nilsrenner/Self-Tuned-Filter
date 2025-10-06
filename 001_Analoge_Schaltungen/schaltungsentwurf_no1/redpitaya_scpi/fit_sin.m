%% Sinosoidal fitting

function s = fit_sin(t,y)
%FIT_SIN Summary of this function goes here
%   Detailed explanation goes here
% Ref. https://de.mathworks.com/matlabcentral/answers/121579-curve-fitting-to-a-sinusoidal-function
% The elements of output parameter vector, s ( b in the function ) are:
% s(1): sine wave amplitude (in units of y)
% s(2): period (in units of t)
% s(3): phase (phase is s(2)/(2*s(3)) in units of t)
% s(4): offset (in units of y)

    yu = max(y);
    yl = min(y);
    yr = (yu - yl);  % Range of 'y', amplitude peak-to-peak
    yz = y - yu + (yr / 2);
    zt = t(yz .* circshift(yz, [0 1]) <= 0);  % Find zero-crossings
    per = 2 * mean(diff(zt));  % Estimate period
    ym = mean(y);  % Estimate offset

    sinfunc = @(b,t)  b(1).*(sin(2*pi*t./b(2) + 2*pi/b(3))) + b(4); % Function to fit
    fcn = @(b) sum((sinfunc(b,t) - y).^2);  % Least-Squares cost function
    s = fminsearch(fcn, [yr;  per;  -1;  ym]);  % Minimise Least-Squares
end    


% Plot/Test of fit
% tp = linspace(min(t),max(t));
% figure(1)
% plot(t, y, 'b', tp, fit_sin(s,tp), 'r')
% grid
