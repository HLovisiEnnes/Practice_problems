i = 999;
j = 999;
c = 0;
done = 0;
while done == 0
    product = num2str(i*j);
    if ~all(product == fliplr(product)) && c == 0
        i = i-1;
        c = 1;
    elseif ~all(product == fliplr(product)) && c == 1
        j = j-1;
        c = 0;
    else
        done = 1;
    end
end


for x = i:999
    for y = j:x
        new_product = num2str(x*y);
        if all(new_product == fliplr(new_product))
            product = new_product;
        end 
    end
end

disp(product)