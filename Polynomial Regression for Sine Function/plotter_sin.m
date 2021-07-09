function plotter_sin(N, d)
%takes as input the number of data points to be generated plus a white
%error and returns plots of the genrator function and the poits, with a
%polynomial regression of degree d, shown green in the plot

%creates the non-noisy dataset to show the genrating function
true_x = 0:0.01:1;
true_y = sin(2*pi*true_x);

%generates the dataset
[x, y] = sin_data_generator(N);

%performs the polynomial regression
prediction = predictor(x, y, d, N, true_x);

%creates the figures
figure 
scatter(x,y)
hold on
plot(true_x,true_y, 'g')
hold on
plot(true_x,prediction, 'r')
ylim([-1.5,1.5])
hold off
end