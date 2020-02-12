lookup = [
    (0, 'harry potter', 1900),
    (1, 'got', 2500),
    (2, 'nesbo', 1000)
]

dictionary = {dic[1] : dic for dic in lookup}
print(dictionary['got'])

#########################

class ClassTest:

    def instance_method(self):
        print('Called instance method {}'.format(self))

    @classmethod
    def class_method(cls):
        print('Called class method of {}'.format(cls))


# Instance must beinitialized
instance = ClassTest()
instance.instance_method()

#Class method can be called directly
ClassTest.class_method()

#########################

class Book:

    TYPES = ('hardcover', 'softcover')

    def __init__(self, name, cover, weight):
        self.name = name
        self.cover = cover
        self.weight = weight

    def __repr__(self):
        print("Book: {}, Cover-Type: {}, Weight: {}g".format(self.name, self.cover, self.weight))
    

    @classmethod
    def hardcover(cls, name, total_weight):
        return (cls(name, cls.TYPES[0], total_weight))

    @classmethod
    def softcover(cls, name, total_weight):
        return (cls(name, str(cls.TYPES[1]), total_weight))


heavy = Book.hardcover('harry potter', 1000)
print(heavy)

light = Book.softcover('Data Science 101', 500)
print(light)

