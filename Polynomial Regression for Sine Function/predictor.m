function prediction = predictor(x, y, d, N, true_x)
%given the predicted parametes w through paramaters, evaluate the
%polynomial model in the non-noisy dataset so to plot the model 

parameters =  parameter_estimator(x, y, d, N);
degrees = 0:d;

%part that actually evaluates the model \sum_{i=0}^D w_i x^i
prediction = [];
for x_index = 1:size(true_x, 2)
    x_value = true_x(x_index);
    x_value = repmat(x_value, 1, d+1);
    parameter_value = x_value.^degrees;
    parameter_value = parameter_value.*parameters;
    result = sum(parameter_value);
    prediction = [prediction, result];
end

end