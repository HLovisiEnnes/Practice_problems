'''
Monte Carlo simulation for calculating the avarage distance between any two points sampled uniformily on a circle of radius R. 
'''
#import relevant libraries
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
import pandas as pd

def sample_circle(number_of_points, R = 1, plot = False):
    '''
    Samples uniformly on a circle of radius R through the algorithm defined on the main paper.
    If plot = True, shows a scatter drawing of the sampled points and the circle of radius R
    Input: number_of_points, R = 1, plot = False
    Output: the x and y coordinates of the sampled points
    '''
    x_coord = []
    y_coord = []
    #sample on the square RxR until we get exactly number_of_points inside the circle
    while(len(x_coord))<number_of_points:
        x = uniform(-R, R)
        y = uniform(-R,R)
        
        #as defined in the main paper, we accept the sampled point if inside the circle of radius R, otherwise reject it
        if np.sqrt(x**2+y**2)< R:
            x_coord.append(x)
            y_coord.append(y)
    
    #plots the sampled points if plot = True, together with the circle of radius R
    if plot == True:
        x_circ = np.linspace(-R, R, 100)
        y_circ_pos = np.sqrt(R**2-x_circ**2)
        y_circ_neg = -np.sqrt(R**2-x_circ**2)
        
        plt.scatter(x_coord, y_coord)
        plt.plot(x_circ, y_circ_pos, c = 'r', linewidth=4)
        plt.plot(x_circ, y_circ_neg, c = 'r', linewidth=4)
        plt.axis("equal")
        plt.title('Uniform Sampling on The Circle of Radius R')
        plt.show()
    
    #transform the coordinates into numpy arrays
    x_coord = np.array(x_coord)
    y_coord = np.array(y_coord)
    x_coord = x_coord.reshape(-1,1)
    y_coord = y_coord.reshape(-1,1)
    coordinates = np.concatenate((x_coord,y_coord),axis=1)
    
    return coordinates

def estimator(number_of_points, R):
    '''
    Samples 2x(number_of_points) on circles of radius R, then calculates the Monte Carlo estimator and its standard deviaton,as
    described in the main paper 
    Input: number_of_points, R
    Output: (Monte Carlo estimator, standard deviation of the Monte Carlo estimator)
    '''
    points_1 = sample_circle(number_of_points, R)
    points_2 = sample_circle(number_of_points, R)
    dist_vector = []
    for i in range(len(points_1)):
        for j in range(len(points_2)):
            dif = points_1[i]-points_2[j]
            dist_vector.append(np.sqrt(np.dot(dif,dif)))
    return (np.mean(dist_vector), np.std(dist_vector))
