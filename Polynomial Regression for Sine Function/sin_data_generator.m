function [points, noised] = sin_data_generator(number_of_points)
%generates a dataset of size number of points from the function sin(2*pi*x)
%plus a Guassian noise of standard deviation 0.3
    points = rand(1,number_of_points);
    unoised = sin(2*pi*points);
    
%creates the white noise and add it to the generated targets of the
%dataset
    noise = 0.3*randn(1, number_of_points);
    noised = unoised + noise;
end 