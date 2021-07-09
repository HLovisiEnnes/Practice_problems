function test_train_error(N, train_size, d_max)
%calculates the train and test MSE error for polynimal regressions of
%degrees 1 to d_max for the generated sine dataset
%the train set has size N*train_size, as 0 < train_size < 1

numb_points = ceil(N*train_size);
[x, y] = sin_data_generator(numb_points);
x_train = x;
y_train = y;

%makes a vector of MSE error for polynomial regressions of degree 0 to
%d_max
error_vec_train = [];
for d = 1:d_max
    prediction = predictor(x_train, y_train, d, numb_points, x);
    error = sqrt(sum((prediction-y).^2)/numb_points);
    error_vec_train = [error_vec_train, error];
end

test_size = 1-train_size;
numb_points_test = ceil(N*test_size);
[x, y] = sin_data_generator(numb_points);

error_vec_test = [];
for d = 1:d_max
    prediction = predictor(x_train, y_train, d, numb_points, x);
    error = sqrt(sum((prediction-y).^2)/numb_points_test);
    error_vec_test = [error_vec_test, error];
end

%plots MSE error
figure
plot(1:d_max, error_vec_train, 'o -')
hold on
plot(1:d_max, error_vec_test, 'o -')
hold off
legend('Train error','Test error')
end
