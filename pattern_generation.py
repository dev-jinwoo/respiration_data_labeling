from random import random, uniform, randint
import matplotlib.pyplot as plt
import numpy as np


def sigmoid(x):
    x = abs(x)
    return 1 / (1 + np.exp(-x))


# 최소 분당 호흡 수, 최대 분당 호흡 수, peak 최소값
res_min, res_max, amplitude = 12, 20, 0.5
respiration_num = randint(res_min, res_max)

# 호흡 하나당 Data 길이
data_length = 1500 // respiration_num
data = np.zeros([data_length])

# peak 위치 및 값 생성
peak = randint(data_length//2 - 5, data_length//2 + 5)
data[peak] = uniform(amplitude, 1)

t = []
# for i in range(len(data)):
#     if i == peak:
#         continue
#     # peak와 가까울 수록 가중치 적게
#     weight = np.tanh(-2*(i-peak))
#     value = uniform(0, 0.005) * weight
#
#     if i != 0 and i - 1 != peak and i + 1 != len(data):
#         data[i] = data[i-1] + value


for i in range(peak, 0, -1):
    weight = 1.2 * (i - peak/2)
    value = uniform(0, 0.005) * weight
    data[i-1] = data[i] - value

# print(data)

print(data_length, peak, data.shape)
print(data)

plt.ylim([-1, 1])
plt.plot(data)
plt.show()
# def generation(res_min, res_max):





# for i in range(110):
#     if i == 0:
#         value = uniform(-1, -0.5)
#         data_list.append(round(value, 8))
#     elif i == peak:
#         value = uniform(0.5, 1)
#         data_list.append(round(value, 8))
#     elif peak - 10 < i < peak + 10:
#         if peak - 10 < i:
#             value = uniform(0, 0.005)
#             data_list.append(round(data_list[i - 1] + value, 8))
#         elif peak + 10 > i:
#             value = uniform(-0.005, 0)
#             data_list.append(round(data_list[i - 1] + value, 8))
#
#     elif i < peak:
#         value = uniform(0, 0.05)
#         data_list.append(round(data_list[i-1] + value, 8))
#     elif i > peak:
#         value = uniform(-0.05, 0)
#         data_list.append(round(data_list[i - 1] + value, 8))
#
#
# plt.plot(data_list)
# plt.show()