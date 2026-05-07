# Data Structures in Python

# List : Use a List when you need an ordered collection of items that can be updated frequently. 
# Lists are mutable, meaning you can change their content after creation. 
# They are ideal for storing collections of items where duplicates are allowed and order matters.
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")  # Thêm phần tử
fruits[0] = "strawberry" # Thay đổi phần tử
print(fruits) # Output: ['strawberry', 'banana', 'cherry', 'orange']

# Tuple : Use a Tuple when you need an ordered collection of items that should not be changed after creation. 
# Tuples are immutable, meaning once they are created, their content cannot be modified.
# They are ideal for storing fixed collections of items, such as coordinates, where immutability is desired.
# Tuples can also be used as keys in dictionaries, while lists cannot.
coordinates = (10.0, 20.5)
# coordinates[0] = 15.0  <-- error: tuples are immutable
print(coordinates[0]) # Output: 10.0    
print(coordinates[1]) # Output: 20.5

# Set: Use a Set when you need an unordered collection of unique items.
# Sets are mutable, but they do not allow duplicate elements.
# They are ideal for storing collections of items where uniqueness is important, such as a collection of unique identifiers or tags.
# Sets also support mathematical operations like union, intersection, and difference.
# Note: Sets are unordered, so they do not maintain the order of elements.
unique_numbers = {1, 2, 3, 4}
unique_numbers.add(5)  # Add a new element
unique_numbers.add(3)  # No effect, since 3 is already in the set
print(unique_numbers) # Output: {1, 2, 3, 4, 5}

# Dictionary: Use a Dictionary when you need to store key-value pairs and access values by their keys.
# Dictionaries are mutable and allow for fast lookups, making them ideal for situations where you need to associate values with unique keys, such as storing user information or configuration settings.
# Note: Dictionaries are unordered in Python versions before 3.7, but from Python 3.7 onwards, they maintain the insertion order of keys.
person = {"name": "Alice", "age": 30}
print(person["name"]) # Output: Alice
person["age"] = 31  # Update value
person["city"] = "New York"  # Add new key-value pair
print(person) # Output: {'name': 'Alice', 'age': 31, 'city': 'New York'}

# Nested data structures are data structures that contain other data structures as their elements.
# They allow you to create more complex and hierarchical data representations.
# For example, you can have a list of dictionaries, a dictionary of lists, or even a dictionary of dictionaries.
# Example of a nested dictionary:
# A nested dictionary is a dictionary that contains another dictionary as its value.
# This allows you to create a hierarchical structure where you can store related information together.
# In this example, we have a nested dictionary that stores information about two people, where each person has their own dictionary containing their name and age.
# To access the name of person1, we use nested_dict["person1"]["name"], which first retrieves the dictionary for person1 and then accesses the "name" key within that dictionary.
nested_dict = {
    "person1": {"name": "Alice", "age": 30},
    "person2": {"name": "Bob", "age": 25}
}
print(nested_dict["person1"]["name"]) # Output: Alice


