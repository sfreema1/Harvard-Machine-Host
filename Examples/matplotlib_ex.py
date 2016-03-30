import matplotlib.pyplot as plt

pop_ages = [22,55,66,3,43,2,3,4,2,4,6,12,3,23,4,4,5,6,34,45,4,5,3,4]
#idx = [x for x in range(len(pop_ages))]

bins = [0,10,20,30,40,50,60,70,80,90,100,120,130]

plt.hist(pop_ages, bins, histtype='bar', rwidth=0.8)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph')
plt.legend()
plt.show()