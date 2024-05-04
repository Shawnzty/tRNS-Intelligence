clc;
clear;

% least and most steps
fs = 4800;
rest_least = 864000;
rest_most = 868800;

for subject_id = 1:26
    for tasktime = 1:2
        if subject_id == 3 && tasktime == 1
           continue 
        elseif subject_id == 11 && tasktime == 1
            continue
        end
        filename = "../../data/" + num2str(subject_id) + "/" + num2str(subject_id) + "_rs" + num2str(tasktime) + ".mat";
        disp(filename);
        eeg = load(filename).y;
        trig = eeg(end,:);
        rest = zeros(1, length(trig)); % event
        
        break_sig = 0;
        head = 1;
        while (break_sig == 0)
            if trig(head) > 5 && trig(head+rest_least) > 5 && trig(head+rest_most) == 0
                break_sig = 1;
                rest(head) = 1; % event
            end
            head = head + 1;
        end
        head = head - 10;
        disp(head);
        
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
        disp(tail);
        disp((tail-head)/(4800*60));
        
        eeg = [eeg; rest];
        eeg = eeg(:,head:tail);
        new_name = "../../data/" + num2str(subject_id) + "/" + num2str(subject_id) + "_rs" + num2str(tasktime) + "_withevent.mat";
        save(new_name, "eeg");
    end
end