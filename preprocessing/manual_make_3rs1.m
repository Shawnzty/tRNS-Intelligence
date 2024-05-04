clc;
clear;

% least and most steps
fs = 4800;
rest_start = 668600; % 668657
rest_end = 812702; % 812702

eeg = load("../../data/3/3_1.mat").y;

one_piece = eeg(2:33,rest_start:rest_end);
one_piece_flip = flip(one_piece, 2);

make_rs = [one_piece one_piece_flip one_piece one_piece_flip one_piece one_piece_flip];
len = length(make_rs);
time = eeg(1,1:len);
trig = zeros(1,len);
need_length = 180*fs;
trig(100:need_length+100) = 8;

rest = zeros(1, len);
rest(100) = 1;

eeg = [time; make_rs; trig; rest];
plot(eeg(2,:))
hold on;
plot(eeg(34,:));

new_name = "../../data/3/3_rs1_withevent.mat";
save(new_name, "eeg");