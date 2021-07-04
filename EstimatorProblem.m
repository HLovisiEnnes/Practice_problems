%the goal of this file is to compare the risk of randomized and
%non-randomized estimator
theta_v_y = [];
theta_v_x = [];

%we will make theta our parameter
for theta = -10:0.1:10
    v_x = [];
    v_y = [];
    
    %we will make 500 iterations so to get an actual close value for the
    %expectation
    for i = 1:500
        b = 100;
        
        %we make x our common estimator for the mean of a normal and
        %calculate the risk of the mean
        x = randn(1,100) + theta;
        x_ave =  mean(x);
        x_risk = mean((theta-x_ave).^2);
        v_x = [v_x, x_risk];
        
        %we have y = N(x_ave,1) and calculate the mean square risk
        y = randn(b,100) + x_ave;        
        y_ave = mean(y');
        y_risk = mean((theta-y_ave).^2);
        v_y = [v_y, y_risk];
    end
    
    %we take the mean so to take a closer value and plot for the values of
    %theta in the range -10:0.1:10
    y_final = mean(v_y);
    theta_v_y = [theta_v_y, y_final];
    
    x_final = mean(v_x);
    theta_v_x = [theta_v_x, x_final];
end

plot(-10:0.1:10, theta_v_x, -10:0.1:10, theta_v_y)
