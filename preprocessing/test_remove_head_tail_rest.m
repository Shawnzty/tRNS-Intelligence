clc;
clear;

% least and most steps
fs = 4800;
rest_least = 780000;
rest_most = 820000;

eeg = load("../../data/11/11_rs1.mat").y;

trig = eeg(end,:)*100;
% time = eeg(1,:);

plot(eeg(2,:));
hold on;
plot(trig);
ylim([-400,1000]);

% detect short resting state
break_sig = 0;
head = 1;
while (break_sig == 0)
    if trig(head) > 5 && trig(head+rest_least) > 5 && trig(head+rest_most) == 0
        break_sig = 1;
    end
    head = head + 1;
end
head = head - 10;

% detect tail
break_sig = 0;
tail = length(trig);
while (break_sig == 0)
    if trig(tail) > 5 && trig(tail-rest_least) > 5 && trig(tail-rest_most) == 0
        break_sig = 1;
    end
    tail = tail - 1;
end
tail = tail + 10;

disp((tail-head)/(4800*60));
new_name = "../../data/11/11_rs1_aligned.mat";
save(new_name, "eeg");




