# example plot for the relu activation function
from matplotlib import pyplot as plt
from math import exp
import numpy as np
import matplotlib.gridspec as gridspec


#
#
# figure, axis = plt.subplots(2, 2)
# # define input data
# inputs = [x for x in range(-10, 10)]
# # calculate outputs
# outputs = [rectified(x) for x in inputs]
#
#
# # sigmoid activation function
# def sigmoid(x):
#     return 1.0 / (1.0 + exp(-x))
#
#
# # derivative ReLU
# def reluderiv(x):
#     if x>=0:
#         return 1
#     elif x<0:
#         return 0
#
#
# outputs2= [reluderiv(x) for x in inputs]
#
#
# G = gridspec.GridSpec(3, 3)
# axes_1 = plt.subplot(G[0, :])
# axes_1.plot(inputs, outputs, 'r-', inputs, outputs2)
# #axis[0,0].plot(inputs, outputs2, 'o-')
# # define input data
# inputs = [x for x in range(-10, 10)]
# # calculate outputs
# outputs = [sigmoid(x) for x in inputs]
# # plot inputs vs outputs
# #axis[0,1].plot(inputs, outputs, 'g-')
# plt.show()

def sigmoid(x):
    s=1/(1+np.exp(-x))
    ds=s*(1-s)
    return s,ds


# rectified linear function
def rectified(x):
    return max(0.0, x)

def reluderiv(x):
    if x>=0:
        return 1
    # elif x<=0:
    #     return 0
    # elif x==0:
    #     return 1
    if x<=0:
        return 0
# define a series of inputs
series_in = [x for x in range(-6, 6)]
# calculate outputs for our inputs
series_out = [rectified(x) for x in series_in]
outputs2= [reluderiv(x) for x in series_in]
# line plot of raw inputs to rectified outputs
# plt.plot(series_in, series_out, series_in, outputs2, 'r-')
x=np.arange(-6,6,0.01)

fig, ax = plt.subplots(figsize=(9, 5))
ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')# Create and show plot
ax.plot(series_in,series_out, color="#307EC7", linewidth=3, label="ReLU")
ax.plot(series_in,outputs2, 'r-', linewidth=3, label="pochodna")
ax.legend(loc="upper right", frameon=False)



x=np.arange(-6,6,0.01)
sigmoid(x)# Setup centered axes
fig, ax = plt.subplots(figsize=(9, 5))
ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')# Create and show plot
ax.plot(x,sigmoid(x)[0], color="#307EC7", linewidth=3, label="sigmoid")
ax.plot(x,sigmoid(x)[1], 'r-', linewidth=3, label="pochodna")
ax.legend(loc="upper right", frameon=False)
plt.show()

