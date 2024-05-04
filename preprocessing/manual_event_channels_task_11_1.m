clc;
clear;

eeg_origin = load("../../data/11/11_1_aligned.mat").eeg;

trig = eeg_origin(34,:);
len = length(trig);

fs = 4800;
rest_least = 144000;
rest_most = 150000;
question_least = 2000;
question_most = 2500;
answer_least = 900;
answer_most = 1200;

% create containers
rest = zeros(1, len);
question = zeros(1, len);
response = zeros(1, len);


% mark start of fixation and stim
pointer = 1;
rest_count = 0;

while pointer <= size(eeg_origin,2)
    if rest_count == 0
        if trig(pointer) > 5 && trig(pointer+rest_least) > 5 && trig(pointer+rest_most) == 0
            rest(pointer) = 1;
            rest_count = 1;
            pointer = pointer + 30*fs;
        end
    end
    
    if pointer+question_most < len
        if trig(pointer) > 5 && trig(pointer+question_least) > 5 && trig(pointer+question_most) == 0
            question(pointer) = 1;
            pointer = pointer + 0.5*fs;
        end
    end
    if pointer+answer_most < len
        if trig(pointer) > 5 && trig(pointer+answer_least) > 5 && trig(pointer+answer_most) == 0
            response(pointer) = 1;
            pointer = pointer + 0.2*fs;
        end
    end
    pointer = pointer + 1;
end

% concatenate
eeg = zeros(37,size(eeg_origin,2));
eeg(1:34,:) = eeg_origin(1:34,:);

eeg(35,:) = rest;
eeg(36,:) = question;
eeg(37,:) = response;

% save eeg data
new_name = "../../data/11/11_1_withevent.mat";
save(new_name, "eeg");

rest = rest*8; question = question*8; response = response*8;
plot(trig);
hold on;
plot(rest); 
plot(question); 
plot(response);
disp(sum(question)/8);
disp(sum(response)/8);
