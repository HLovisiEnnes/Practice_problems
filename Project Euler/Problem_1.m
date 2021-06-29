mult_3 = 0:3:999;
mult_5 = 0:5:999;

mult_3_5 = set_maker([mult_3, mult_5]); %takes away repeating values
disp(sum(mult_3_5))

function list = set_maker(x) 
%makes a set out of a list (i.e. excludes repeating values)
list = [];
for y = x
    if ismember(y, list) == 0
        list = [list, y];
    end
end
end