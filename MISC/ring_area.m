outer_dia = 45; % mm
inner_dia = 15; % mm

outer_r = (outer_dia/10)/2;
inner_r = (inner_dia/10)/2;

area = pi*(outer_r^2 - inner_r^2);
disp(area);