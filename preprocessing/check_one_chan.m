clear;
clc;
close all;

filename = "shi_11_2";
filename = append("../../data/eeg/",filename);
eeg = load(filename).y;

% Sampling frequency
Fs = 4800;

% Design a bandpass filter with cutoff frequencies of 0.1 Hz and 100 Hz
[b, a] = butter(2, [0.1 50] / (Fs / 2), 'bandpass');

% Preallocate the filtered EEG data matrix
filteredEEG = zeros(size(eeg));

% Copy the time, EOG, and trigger signal rows to the new matrix as is
filteredEEG([1, 33:34], :) = eeg([1, 33:34], :);

% Apply the bandpass filter to each EEG channel
for i = 2:32
    filteredEEG(i, :) = filtfilt(b, a, eeg(i, :));
end

% Plot raw
time = eeg(1, :); % Time stamps
plot(time, filteredEEG(34,:));
% ylim([-50 50]);
% xlim([205 217]);

% for chan = 1:32
%     figure(); % Create a new figure window
% 
%     plot(time, filteredEEG(chan+1,:));
%     hold on;
%     plot(time, filteredEEG(34,:));
% 
%     ylim([-50 50]);
%     xlim([205 217]);
% 
% end

% Plot raw
% time = eeg(1, :); % Time stamps
% for chan = 1:32
%     % figure(); % Create a new figure window
%     t1 = 288000;
%     t2 = 288000*4;
%     x = filteredEEG(chan+1, t1:t2);
% 
%     figure();
%     [freq,db] = getPSD(x,Fs);
%     plot(freq,db)
%     % ylim([-50 50]);
%     xlim([0 50]);
% 
% end
