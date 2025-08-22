## Family Tree Handling System

This project is a Python-based Family Tree Management System developed
in three versions (F1, F2, F3).
Each version adds new features to handle family relationships and
provides an interactive menu for the user.

## Version 1 -- finalf1.py

This is the foundation of the project.
Features: - Add people (with birth and optional death dates).Create
relationships like parent-child and spouses. Explore family
connections: - Parents - Siblings - Grandparents - Grandchildren -
Immediate family - Extended family (aunts, uncles, cousins).

It also has an interactive menu where you pick a family member and see
their details.

## Version 2 -- f2final.py

Adds extra features to make the family tree more interactive: - Check
siblings of a person. - See cousins (with their parents and spouses).
View birthdays of specific family members. Generate a birthday
calendar for the whole family.

## Version 3 -- f3final.py

The most advanced version.
Includes everything from F1 & F2, plus analytics and statistics: 
Average age at death (for deceased family members). Average number of
children per person. Number of children for a chosen family member.
A detailed birthday calendar.

## How to Run

1. Make sure you have Python 3.8+ installed.
2. Clone or download the project.
3. Run one of the versions in your terminal:

``` bash
python finalf1.py   # Run Version 1
python f2final.py   # Run Version 2
python f3final.py   # Run Version 3
```

## Project Structure

    ├── finalf1.py   # Basic Family Tree (parents, siblings, extended family)
    ├── f2final.py   # Adds birthdays and cousin features
    ├── f3final.py   # Adds stats and advanced calendar
    └── README.md    # Documentation

## Example

  Run the program
  Pick a family member from the list
  Explore details such as:
  Parents, siblings, spouse, children
  Cousins and their parents
  Birthday calendars
  Family statistics (F3)

## Future Improvements

  Add a graphical interface (Tkinter or Flask web app).
  Import/export family data in JSON or CSV.
  Visualize the tree using Graphviz or NetworkX.

This project was a way to practice object-oriented programming in Python
while also building something practical and relatable: a digital family
tree.