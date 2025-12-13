class A:
    def say(self):
        print("A")


class B:
    def say(self):
        print("B")


class C(A, B):
    pass


c = C()
c.say()
print(C.mro())

# Notes -
# 🧠 How Python makes it sane (MRO)
# Python uses something called the C3 linearization algorithm to decide:
#     which class to look at first
#     how to walk the diamond hierarchy
#     how to avoid ambiguity
# You can see the order with:
C.mro()


# Why Python allows it:
#     trust the developer
#     give the language a consistent rule system (MRO)
#     let advanced programmers build powerful abstractions when needed
# It works beautifully.
# ⚠️ When not to use it
# Same rule as in any language:
# Don’t use multiple inheritance unless it provides a real design advantage.
# Use cases where it shines:
#     mixins (most common)
#     combining orthogonal behaviors
#     decorating classes with small capabilities
#     frameworks that need pluggable behavior
#     GUI toolkits (Tkinter, PyQt, Django CBVs, etc.)
class WalkMixin:
    def walk(self):
        print("Walking")


class TalkMixin:
    def talk(self):
        print("Talking")


class Person(WalkMixin, TalkMixin):
    pass


# A GUI widget that is both a “visual component” and an “event source”
# A lot of GUI frameworks (Qt, Tkinter patterns, old wxPython) use this exact structure.
# Hierarchy 1: Visual components
# Widget
#  ├── Button
#  ├── Label
#  └── TextBox
# Hierarchy 2: Event sources
# EventEmitter
#  ├── Clickable
#  ├── Draggable
#  └── Focusable
# The diamond occurs naturally:
class Button(Widget, Clickable):
    pass


# Why it makes sense:
#     Button is a widget
#     Button is clickable
#     Both hierarchies represent real, orthogonal concepts
#     The behaviors don’t conflict
# This is one of the cleanest practical uses of multiple inheritance.
# Example 2
# ⭐ 2. A network object that is both “Serializable” and “Validatable”
# Imagine you're designing models for an API.
# Hierarchy 1: Serialization behavior
# Serializable
#  ├── JSONSerializable
#  └── BinarySerializable
# Hierarchy 2: Domain validation
# Validatable
#  ├── UserValidatable
#  └── OrderValidatable
# Now define a clean data model:
class User(JSONSerializable, UserValidatable):
    pass


# This works beautifully because the two behaviors are independent:
#     Serialization → how data is converted
#     Validation → how data is checked
# They don’t overlap, and MRO handles ordering cleanly.
# Example 3.
# ⭐ 3. An AI model layer that is both “Trainable” and “Inspectable”
# This one you’ll actually see in ML codebases.
# Hierarchy 1: Model type
# Layer
#  ├── Dense
#  ├── Conv
#  └── Recurrent
# Hierarchy 2: Inspectability (debugging utilities)
# Inspectable
#  ├── ActivationsInspectable
#  └── GradientsInspectable
# Now you combine them:
class InspectableDense(Dense, ActivationsInspectable):
    pass


# This is extremely useful when debugging neural nets.
# Why it makes sense:
#     Dense defines forward/backward logic
#     Inspectable adds hooks and logging
# They don’t represent the same conceptual axis.
# 🧠 The pattern behind all these: orthogonality
# Multiple inheritance is correct when each parent provides completely different, non-conflicting responsibilities.
# Think of it as:
#     one parent gives you what you are
#     the other gives you something you can also do
#     This is why mixins are so successful:
#     they are tiny, orthogonal behaviors.
# But occasionally — rarely — you get legitimately separate full hierarchies that both make conceptual sense.

# 🔥 The litmus test for “good” multiple inheritance
# Ask:
# Do these two parents represent different dimensions of responsibility,
# not two competing definitions of the same thing?

# If yes → It’s clean.
# If no → It’s a road to madness.
# Python simply says:

# “A class can inherit from any number of bases.
# You handle the meaning; I’ll handle the MRO.”
# No forced hybrid interface.
# No interface soup.
# No need to create types just because the language can’t express the idea.
# This gives you clean, orthogonal behavior composition.


# 🪞 Why this matters for you specifically
# You’re learning Python properly, not the “copy/paste and pray” style.
# Understanding these patterns now means you will naturally:
#     avoid Java-style over-engineering
#     model your code around behaviors, not hierarchies
#     write mixin-style components where appropriate
#     keep your classes small, expressive, and orthogonal
# This is exactly the mindset shift that makes Python feel elegant.
class WalkableMixin:
    def walk(self):
        return f"{self.name} is walking."


class FlyableMixin:
    def fly(self):
        return f"{self.name} is flying."


class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal, WalkableMixin):
    pass


class Bird(Animal, WalkableMixin, FlyableMixin):
    pass


class Snake(Animal):
    pass


d = Dog("Rufus")
b = Bird("Robin")
s = Snake("Nagini")

print(d.walk())  # Rufus is walking.
print(b.fly())  # Robin is flying.
print(b.walk())  # Robin is walking.

# 🔥 Why this example makes sense for multiple inheritance
# Because "walk" and "fly" describe capabilities, not types.
# No redundant code.
# No boilerplate.
# No “combined interfaces.”
# Just clean, composable behavior.
# ⭐ Why this matters

# This is exactly the kind of scenario where Python’s multiple inheritance feels natural:
# Capabilities
# Traits
# Behaviors
# Orthogonal functionality
# Reusable, pluggable modules
# Not UI junk.
# Not serialization frameworks.
# Not complex event systems.
# Just plain logic and real-world modeling.

# A subclass does not need to define an __init__ method if it doesn’t need to do anything extra beyond what the base class already does.
from enum import Enum
from abc import ABC, abstractmethod

Category = Enum("Category", ("Dog", "Cat", "Lion", "Tiger"))


class Animal(ABC):
    def __init__(self, name: str, category: Category):
        self.name = name
        self.category = category

    @abstractmethod
    def make_sound(self) -> str:
        """All animals must make sound."""
        pass


class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof!"


# ✅ This is perfectly fine. Here’s why:

# Inheritance of __init__
# Dog inherits from Animal, so if you don’t define an __init__, Python automatically uses Animal.__init__.
# You only need to write an __init__ in Dog if you want to add new attributes or change initialization behavior.

# Abstract method requirement
# The only requirement for Dog is to implement all abstract methods (make_sound).
# Once you implement them, you can instantiate the class:
my_dog = Dog("Buddy", Category.Dog)
print(my_dog.name)  # Buddy
print(my_dog.category)  # Category.Dog
print(my_dog.make_sound())  # Woof!


# Optional __init__ in subclass
# If later you want Dog to have a breed attribute:
class Dog(Animal):
    def __init__(self, name: str, category: Category, breed: str):
        super().__init__(name, category)
        self.breed = breed
