from enum import Enum

# Using a dictionary for member names and values
Status = Enum("Status", {"OK": 200, "NOT_FOUND": 404, "ERROR": 500})

print(Status.OK)
print(Status.NOT_FOUND.value)

# Using a list of names (values will be assigned automatically, starting from 1)
Fruits = Enum("Fruits", ["APPLE", "BANANA", "ORANGE"])

print(Fruits.APPLE.value)  # Output: 1
print(Fruits.BANANA.name)


class Category(Enum):
    DOG = 1
    CAT = 2
    LION = 3
    TIGER = 4


class Animal:
    def __init__(self, category, age):
        self.category = category
        self.age = age


print(Category.mro())  # Method Resolution Order -- works for classes too.
# Notes
# 1. Enum members compare by identity.
Category.DOG is Category.DOG  # True
# 2. They’re type-safe
# You can’t accidentally pass "dog" where a Category.DOG is expected.
# 3. You can iterate them
for c in Category:
    print(c)
# 4. They’re hashable(immutable)
# Useful for dict keys or sets.
# If you want them uppercase but with lowercase values


class Category(Enum):
    DOG = "dog"
    CAT = "cat"


# or even-
from enum import auto


class Category(Enum):
    DOG = auto()
    CAT = auto()


# Enforce valid values-
class Animal:
    def __init__(self, name, category: Category):
        if not isinstance(category, Category):
            raise ValueError("category must be a Category enum")
        self.name = name
        self.category = category


# Enums are more like singleton constants (created once- reused everywhere) wrapped in a named type.
# Each member is:
#     unique
#     hashable
#     a tiny object with identity
#     accessible by name
#     validated by Python
# Enum members can absolutely have behavior


class Category(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"

    def sound(self):
        if self is Category.DOG:
            return "Woof!"
        elif self is Category.CAT:
            return "Meow!"
        elif self is Category.BIRD:
            return "Chirp!"


# Usage:
print(Category.DOG.sound())  # Woof!
print(Category.CAT.sound())  # Meow!
# You can even give each enum constant its own behavior


class Category(Enum):
    DOG = ("dog", "Woof!")
    CAT = ("cat", "Meow!")
    BIRD = ("bird", "Chirp!")

    def __init__(self, label, sound):
        self.label = label
        self._sound = sound

    def sound(self):
        return self._sound


Category.DOG.sound()  # "Woof!"
Category.CAT.sound()  # "Meow!"

# Can override methods per member


class Category(Enum):
    DOG = ("dog", lambda: "Woof!")
    CAT = ("cat", lambda: "Meow!")

    def __init__(self, label, speak_func):
        self.label = label
        self._speak = speak_func

    def speak(self):
        return self._speak()


# Why add behavior to enums?
# This is especially clean when you have:
#     type-specific serialization
#     formatting rules
#     domain behavior (e.g., tax rate for a product category)
#     classification logic
# You avoid scattering logic across if/elif/elif blocks.

# Class-based Enum:

# class Animal(Enum):          <-- class name, exists as variable too
#     Dog = 1
#     Cat = 2

# Reference for subclassing: Animal
# Variable name: Animal
# Internal class name: Animal (same as variable)

# Subclassing works:
# class Pet(Animal):
#     Rabbit = 3


# Dynamic Enum:

# Outside = Enum("Inside", ("Dog", "Cat"))  <-- variable points to class
#                                             internal name = "Inside"

# Reference for subclassing: Outside (the variable)
# Variable name: Outside
# Internal class name: "Inside" (metadata only)

# Subclassing works:
# class Pet(Outside):
#     Lion = 2

# Cannot use internal name "Inside" as variable:
# class Pet(Inside):  <-- ❌ NameError
#     Lion = 2
# Always use the same variable name as the internal name for the enums.
# Category = Enum("Category", ("Dog", "Cat", "Lion", "Tiger"))
# The first string ("Category") matches the variable name (Category) so that when you print or inspect it, the names line up and it’s easy to read.

# It’s purely for readability and debugging.

# If you gave them different names:
# X = Enum("Animals", ("Dog", "Cat"))
# The variable you use is X.
# The internal class name is "Animals".
# Printing a member shows Animals.Dog, which can be confusing if your variable is called X.
# So, giving them the same name is just a convention to keep things clean and intuitive.
