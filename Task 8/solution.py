
def bootstrap_this(data):
    import numpy as np
    import random

    #number of elements in the array
    N = len(data)

    #number of samples
    samples = 1000

    #distribution of mean values from each sample
    means_list = []

    for i in np.arange(samples):
        new_sample = [] #here I will save the elements of the new sample
        for j in np.arange(N):
            index = random.randint(0,N-1) #generates a random integer between 1 and N
            new_sample.append(data[index]) #adds a random value from the initial sample to the new sample
        means_list.append(np.mean(new_sample)) #computes and save the mean of the new sample
    
    value = np.mean(means_list) #mean of the distribution of means
    error = np.std(means_list) #error of the distribution of means    
    means = np.array(means_list)

    return value, error, means


