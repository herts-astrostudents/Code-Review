# Task 10: Useful Objects with Spectrophotometry

## Colour-Colour diagnostic diagrams
Colour is sometimes useful in separating different types of galaxy. like the BPT emission line diagrams, Colour-Colour diagrams can separate star-forming galaxies, quasars, and stars using their optical colours.


## The Task

The task is to classify the given spectrum as QSO or star using the SDSS(g-r vs u-g) colour-colour diagram.

The task is to finish up the included code which allows a spectrum to be plotted onto a colour-colour diagram. There isn't actually much to do other than fill in the blanks where you see `NotImplementedError`!

The script `run.py` will read in the mystery spectrum and three filter curve files.

The spectra are then propagated through the transmission filters that SDSS uses.

Finally, it plots the magnitude that it gets onto the Colour-Colour diagram. 

We're going to be using objects for this task. It makes code really readable and easy to use. You know exactly what is happening in the code because it essentially explains itself. 

Hopefully, this example shows that it is actually quite easy to structure your code this way once you get used to it. It is much better than having one long script since it is readable, repeatable, and re-usable (as in you can use your Spectrum objects for lots of other things!)


## Objects
Everything in python is an object. This means every variable *has* attributes which can be accessed with the dot: `object.attribute`.

Objects can also *inherit* traits from other objects.

Consider the `list` in python. To look at its attributes call `dir(list)`

    >>> dir(list)

    ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']

We can make a new *type* of object called `MyList` which has a method (function of an object) called `count_ints`.

    class MyList(List):
        def count_ints(self):
            return sum([isinstance(i, int) for i in self])


The new object, `MyList`, has all the same attributes as `list` but also has `count_ints` as well!

    >>> my_list = MyList([1,2,3,'a','b', {}, object])
    >>> len(my_list)
    7
    >>> my_list.count_ints()
    3

Try this short [tutorial](https://www.codecademy.com/courses/learn-python/lessons/introduction-to-classes/exercises/why-use-classes ) if like.





