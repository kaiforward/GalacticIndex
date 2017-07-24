class Test(object):  # Planet class creates all variables for individual planets
    # The class "constructor"
    def __init__(self):
        self.nested_lists = [[0]*10, [0]*10, [0]*10]

object_holder = [[]]*30

for x in xrange(0, 30):
    object_holder[x] = Test()

for objects in xrange(0, 30):
    for lists in xrange(0, 3):
        for items in xrange(0, 10):
            t = object_holder[objects].nested_lists
            y = t[lists]
            y[items] +=1

object_holder[1].nested_lists[0][8] += 5
object_holder[1].nested_lists[2][5] += 12

print object_holder[1].nested_lists
print object_holder[1].nested_lists[0]
print object_holder[1].nested_lists[0][8]
print object_holder[1].nested_lists[2][5]
print object_holder[1].nested_lists[0][5]

print object_holder[2].nested_lists
print object_holder[2].nested_lists[0]
print object_holder[2].nested_lists[0][8]
print object_holder[2].nested_lists[2][5]

