function parameters = parameter_estimator(x, y, d, N)
%estimates the parameters of a degree d fit for the genrated dataset

%vector of powers from 0 to d
degrees = 0:d;

%degree_x is a matrix of size N x d in which we have each row with values from 0 to d, so
%to be used to raise all x values from 0 to d (matrix = x_coef.^degree_x), stored in x_coef
degree_x = repmat(degrees, N, 1);
x_coef = repmat(x', 1, d+1); 
matrix = x_coef.^degree_x;

%estimates the parameters using a linear regression of form Ax = b, where
%we calculate A by Penrose pseudo inverse method
parameters = matrix\y';
parameters = parameters';
end