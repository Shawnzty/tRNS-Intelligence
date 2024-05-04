clc;
clear;

% least and most steps
fs = 4800;
rest_least = 144000;
rest_most = 150000;
question_least = 2000;
question_most = 2500;
answer_least = 900;
answer_most = 1200;

for subject_id = 11:11
    for tasktime = 1:1
        filename = "../../data/" + num2str(subject_id) + "/" + num2str(subject_id) + "_" + num2str(tasktime) + ".mat";
        disp(filename);
        eeg = load(filename).y;
        trig = eeg(end,:);
        
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
        disp(head);
        
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
        tail_ques = tail_ques - 0.5*fs + 90*fs + 1000; % 1000 to prevent outflow in event program
        
        break_sig = 0;
        tail_ans = length(trig);
        while (break_sig == 0)
            if trig(tail_ans) > 5 && trig(tail_ans-answer_least) > 5 && trig(tail_ans-answer_most) == 0
                break_sig = 1;
            end
            tail_ans = tail_ans - 1;
        end
        tail_ans = tail_ans + 1000; % 1000 to prevent outflow in event program
        
        if tail_ans < end_of_ques
            tail = tail_ques;
        else
            tail = min(tail_ques, tail_ans);
        end

        disp(tail);
        disp((tail-head)/(4800*60));

        eeg = eeg(:,head:tail);
        new_name = "../../data/" + num2str(subject_id) + "/" + num2str(subject_id) + "_" + num2str(tasktime) + "_aligned.mat";
        save(new_name, "eeg");
    end
end