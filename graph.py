import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
reddot, = plt.plot([1,2,3,4], [1,4,9,16], 'ro')
greendot, = plt.plot([1,2,3,4], [16,9,4,1], 'go')
plt.axis([0, 6, 0, 20])
plt.xlabel('Nodes')
plt.ylabel('Runtime (ms)')
plt.title('Problem 2 Results')
plt.legend([reddot, greendot], ["By Slot", "By Node"])
plt.savefig('graphoutput.pdf')

