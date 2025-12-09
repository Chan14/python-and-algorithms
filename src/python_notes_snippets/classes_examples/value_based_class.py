# In Python, the concept of abstract classes exists through the abc module.
# An abstract class is a class that cannot be instantiated directly.
# It can define abstract methods (methods that must be implemented by subclasses).
from abc import ABC, abstractmethod
from enum import Enum


class Category(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"


class Animal(ABC):
    def __init__(self, name: str, category: Category):
        self.name = name
        self.category = category

    @abstractmethod
    def speak(self) -> str:
        """All animals must implement a speak method"""
        pass


# Here:
# Animal is abstract — you cannot do Animal("Some", Category.DOG).
# Any subclass must implement speak.
class Dog1(Animal):
    def speak(self):
        return "Woof!"


Dog1("Rex", Category.DOG).speak()  # "Woof!"

# 2️⃣ Equality for value classes


# Python has default equality: obj1 == obj2 checks object identity, not values.
# For value classes, you usually want structural equality.
# You override __eq__:
class Dog2(Animal):
    def speak(self):
        return "Woof!"

    def __eq__(self, other):
        if not isinstance(other, Dog2):
            return False
        return (self.name, self.category) == (other.name, other.category)


Dog2("Rex", Category.DOG) == Dog2("Rex", Category.DOG)  # True
Dog2("Rex", Category.DOG) == Dog2("Max", Category.DOG)  # False
print(Dog2("Rex", Category.DOG) == Dog2("Rex", Category.DOG))
print(Dog2("Rex", Category.DOG) == Dog2("Max", Category.DOG))


# 3️⃣ Hashable classes (usable as dict keys or in sets)
# Python requires that objects which implement __eq__ and are intended to be hashable also implement __hash__.
# Rule:
# If a == b, then hash(a) == hash(b).
# Example:
class Dog3(Animal):
    def speak(self):
        return "Woof!"

    def __eq__(self, other):
        if not isinstance(other, Dog3):
            return False
        return (self.name, self.category) == (other.name, other.category)

    def __hash__(self):
        return hash((self.name, self.category))

    def __repr__(self):
        return f"Dog3(name={self.name!r}, category={self.category!r})"


d1 = Dog3("Rex", Category.DOG)
d2 = Dog3("Rex", Category.DOG)

animal_set = {d1, d2}  # only one entry because they are equal
print(len(animal_set))
d = Dog3("Rex", Category.DOG)
print(d)  # Dog(name='Rex', category=<Category.DOG: 'dog'>)

# 5️⃣ Notes on abstract base classes + value semantics
# If your base class is abstract, it usually doesn’t define __eq__ or __hash__.
# Concrete subclasses implement them based on the actual fields.
# Python doesn’t force you to implement getters/setters; direct attribute access is fine.
# For immutable value classes, you can make attributes read-only using @property.
# 6️⃣ Python tip:
# For pure value classes, Python 3.7+ has dataclasses, which do most of this automatically.
from dataclasses import dataclass


@dataclass(frozen=True)
class Dog4:
    name: str
    category: Category

    def speak(self):
        return "Woof!"


# frozen=True → immutable
# __eq__ and __hash__ automatically derived
# __repr__ automatically derived
# ✅ Very handy for ADTs/value classes.

# So to summarize for equality & hashing:
# Method	Purpose
# __eq__	Compare instances by content, not identity
# __hash__	Make instances usable in sets/dicts, must match __eq__
# __repr__	Debug-friendly string
# __str__	User-friendly string (optional)
