import numpy

# arg = numpy.array([1, 2, 3])
# print arg, arg[-1]
# numpy.roll(arg, -1)
# print arg, arg[-1]

print numpy.__version__

arr = numpy.arange(10)
print arr
newarr = numpy.roll(arr, 2)
print newarr
