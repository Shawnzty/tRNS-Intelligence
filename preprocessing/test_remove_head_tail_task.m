% least and most steps
fs = 4800;
rest_least = 144000;
rest_most = 150000;
question_least = 2300;
question_most = 2700;
answer_least = 950;
answer_most = 1400;

eeg = load("../../data/1/1_1.mat").y;

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
tail_ques = length(trig);
while (break_sig == 0)
    if trig(tail_ques) > 5 && trig(tail_ques-question_least) > 5 && trig(tail_ques-question_most) == 0
        break_sig = 1;
    end
    tail_ques = tail_ques - 1;
end
end_of_ques = tail_ques;
tail_ques = tail_ques - 0.5*fs + 90*fs;

break_sig = 0;
tail_ans = length(trig);
while (break_sig == 0)
    if trig(tail_ans) > 5 && trig(tail_ans-answer_least) > 5 && trig(tail_ans-answer_most) == 0
        break_sig = 1;
    end
    tail_ans = tail_ans - 1;
end
tail_ans = tail_ans + 10;

if tail_ans < end_of_ques
    tail = tail_ques;
else
    tail = min(tail_ques, tail_ans);
end



