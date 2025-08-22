from collections import defaultdict
from datetime import datetime
class Person:
    def __init__(self, name, birth_date, death_date=None):
        self.name = name  # Person's name
        self.birth_date = birth_date  # Date of birth
        self.death_date = death_date  # Date of death (if applicable)
        self.parents = []  # List of parents
        self.siblings = []  # List of siblings
        self.children = []  # List of children
        self.spouse = None  # Spouse

    def add_parent(self, parent):
        """Add a parent and establish relationships."""
        if parent not in self.parents:
            self.parents.append(parent)
            if self not in parent.children:
                parent.children.append(self)

            # Automatically add siblings from parent's children
            for sibling in parent.children:
                if sibling is not self and sibling not in self.siblings:
                    self.add_sibling(sibling)

    def add_sibling(self, sibling):
        """Add a sibling relationship."""
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            if self not in sibling.siblings:
                sibling.siblings.append(self)

    def set_spouse(self, spouse):
        """Set spouse relationship."""
        if self.spouse is None:
            self.spouse = spouse
            spouse.spouse = self

    def get_grandchildren(self):
        """Return a list of grandchildren's names."""
        grandchildren = []
        for child in self.children:
            for grandchild in child.children:
                grandchildren.append(grandchild.name)
        return grandchildren if grandchildren else ["No grandchildren"]

    def get_person_family(self):
        """Retrieve immediate family details."""
        return {
            "Parents": [parent.name for parent in self.parents] if self.parents else ["No parents"],
            "Siblings": [sibling.name for sibling in self.siblings] if self.siblings else ["No siblings"],
            "Spouse": [self.spouse.name if self.spouse else "No spouse"],
            "Children": [child.name for child in self.children] if self.children else ["No children"],
        }

    def __str__(self):
        """String representation of a person."""
        return f"{self.name} (Born: {self.birth_date}, Died: {self.death_date if self.death_date else 'Alive'})"

class FamilyTree:
    def __init__(self):
        """Initialize a FamilyTree object."""
        self.members = {}

    def add_member(self, name, birth_date, death_date=None):
        """Add a new member to the family tree."""
        if name not in self.members:
            self.members[name] = Person(name, birth_date, death_date)
        return self.members[name]

    def add_relationship(self, parent_name, child_name):
        """Add a parent-child relationship."""
        if parent_name in self.members and child_name in self.members:
            parent = self.members[parent_name]
            child = self.members[child_name]
            child.add_parent(parent)

    def set_spouse(self, name1, name2):
        """Set a spouse relationship."""
        if name1 in self.members and name2 in self.members:
            self.members[name1].set_spouse(self.members[name2])

    def calculate_average_age_at_death(self):
        """Calculate the average age at death for deceased members."""
        total_age = 0
        deceased_count = 0
        for member in self.members.values():
            age = member.calculate_age_at_death()
            if age:
                total_age += age
                deceased_count += 1
        return total_age / deceased_count if deceased_count > 0 else None

    def calculate_average_children_per_person(self):
        """Calculate the average number of children per person."""
        total_children = sum(len(member.children) for member in self.members.values())
        total_people = len(self.members)
        return total_children / total_people if total_people > 0 else 0

    def get_children_count(self, name):
        """Get the number of children for a specific person."""
        if name in self.members:
            return len(self.members[name].children)
        return 0

    def get_birthday_calendar(self):
        """Generate a birthday calendar."""
        calendar = defaultdict(list)
        for member in self.members.values():
            birth_month_day = datetime.strptime(member.birth_date, "%Y-%m-%d").strftime("%m-%d")
            calendar[birth_month_day].append(member.name)
        return calendar

    def display_birthday_calendar(self):
        """Display the birthday calendar."""
        calendar = self.get_birthday_calendar()
        print("\nBirthday Calendar:")
        for date, members in sorted(calendar.items()):
            print(f"[{date}]: {', '.join(members)}")

# Updated Menu System
if __name__ == "__main__":
    family_tree = FamilyTree()



    # Add family members
    family_tree.add_member("Ali", "1940-06-21", "2002-05-24")
    family_tree.add_member("Fatemeh", "1945-09-01")
    family_tree.add_member("Mohammad", "1970-11-09")
    family_tree.add_member("Maryam", "1975-04-30")
    family_tree.add_member("Reza", "2000-05-08")
    family_tree.add_member("Sara", "2001-07-15")
    family_tree.add_member("Iman", "2004-11-21","2018-12-30")
    family_tree.add_member("Leila", "2014-07-01")
    family_tree.add_member("Irfan", "2003-04-22")
    family_tree.add_member("Mehran", "2005-12-08")
    family_tree.add_member("Qazi Eisa", "2009-01-01") # Granddaughter (Reza's child)

    # Build relationships for the first family group
    family_tree.members["Ali"].set_spouse(family_tree.members["Fatemeh"])
    family_tree.members["Mohammad"].add_parent(family_tree.members["Ali"])
    family_tree.members["Mohammad"].add_parent(family_tree.members["Fatemeh"])

    family_tree.members["Mohammad"].set_spouse(family_tree.members["Maryam"])
    family_tree.members["Reza"].add_parent(family_tree.members["Mohammad"])
    family_tree.members["Reza"].add_parent(family_tree.members["Maryam"])

    family_tree.members["Sara"].add_parent(family_tree.members["Mohammad"])
    family_tree.members["Sara"].add_parent(family_tree.members["Maryam"])

    family_tree.members["Iman"].add_parent(family_tree.members["Mohammad"])
    family_tree.members["Iman"].add_parent(family_tree.members["Maryam"])

    family_tree.members["Leila"].add_parent(family_tree.members["Reza"])

    # Inserting second family group
    family_tree.add_member("Hamza", "1940-12-21")  # Grandfather
    family_tree.add_member("Bibi Gul", "1945-07-09")  # Grandmother

    family_tree.add_member("Asad", "1970-04-06")  # Father
    family_tree.add_member("Zainab", "1975-09-04")  # Mother
    family_tree.add_member("Khan", "1968-09-17")  # Uncle
    family_tree.add_member("Samina", "1980-06-01")  # Aunt

    family_tree.add_member("Ali", "2000-04-07")  # Son
    family_tree.add_member("Aisha", "2003-05-04")  # Daughter
    family_tree.add_member("Bilal", "2005-03-19")  # Son

    family_tree.add_member("Saif", "1998-07-01")  # Cousin (Khan's son)
    family_tree.add_member("Sadia", "2002-11-01")  # Cousin (Khan's daughter)
    family_tree.add_member("Omer", "2007-01-01")  # Cousin (Khan's son)

    family_tree.add_member("Fatima", "2025-02-01")  # Granddaughter (Aisha's child)
    family_tree.add_member("Hassan", "2000-10-10")  # Aisha's spouse

    family_tree.add_member("Ahmad", "1973-03-15")  # Distant uncle (Hamza's younger brother)
    family_tree.add_member("Shabana", "1978-08-22")  # Ahmad's wife
    family_tree.add_member("Nida", "2001-02-18")  # Ahmad and Shabana's daughter

    # Build relationships for the second family group
    family_tree.members["Hamza"].set_spouse(family_tree.members["Bibi Gul"])
    family_tree.members["Asad"].add_parent(family_tree.members["Hamza"])
    family_tree.members["Asad"].add_parent(family_tree.members["Bibi Gul"])
    family_tree.members["Khan"].add_parent(family_tree.members["Hamza"])
    family_tree.members["Khan"].add_parent(family_tree.members["Bibi Gul"])
    family_tree.members["Ahmad"].add_parent(family_tree.members["Hamza"])
    family_tree.members["Ahmad"].add_parent(family_tree.members["Bibi Gul"])

    family_tree.members["Asad"].set_spouse(family_tree.members["Zainab"])
    family_tree.members["Ali"].add_parent(family_tree.members["Asad"])
    family_tree.members["Ali"].add_parent(family_tree.members["Zainab"])

    family_tree.members["Aisha"].add_parent(family_tree.members["Asad"])
    family_tree.members["Aisha"].add_parent(family_tree.members["Zainab"])

    family_tree.members["Bilal"].add_parent(family_tree.members["Asad"])
    family_tree.members["Bilal"].add_parent(family_tree.members["Zainab"])

    family_tree.members["Aisha"].set_spouse(family_tree.members["Hassan"])
    family_tree.members["Fatima"].add_parent(family_tree.members["Aisha"])
    family_tree.members["Fatima"].add_parent(family_tree.members["Hassan"])

    family_tree.members["Khan"].set_spouse(family_tree.members["Samina"])
    family_tree.members["Saif"].add_parent(family_tree.members["Khan"])
    family_tree.members["Saif"].add_parent(family_tree.members["Samina"])

    family_tree.members["Sadia"].add_parent(family_tree.members["Khan"])
    family_tree.members["Sadia"].add_parent(family_tree.members["Samina"])

    family_tree.members["Omer"].add_parent(family_tree.members["Khan"])
    family_tree.members["Omer"].add_parent(family_tree.members["Samina"])

    family_tree.members["Ahmad"].set_spouse(family_tree.members["Shabana"])
    family_tree.members["Nida"].add_parent(family_tree.members["Ahmad"])
    family_tree.members["Nida"].add_parent(family_tree.members["Shabana"])


    def list_members():
        """Display all members and return a map of indexes to names."""
        print("\nSelect a person:")
        index_map = {}
        for i, name in enumerate(family_tree.members.keys(), 1):
            print(f"{i}: {name}")
            index_map[i] = name
        return index_map


    while True:
        print("\n--- Family Tree Menu ---")
        print("1: View a person's immediate family")
        print("2: View cousins with parents")
        print("3: View birthday")
        print("4: View birthday calendar")
        print("5: Average age at death")
        print("6: Number of children for a person")
        print("7: Average number of children per person")
        print("8: View a person's parent(s) name")
        print("9: View a person's siblings")
        print("10: View a person's grandchildren")
        print("11: Exit")

        choice = input("Choose an option: ").strip()

        if choice in {"1", "2", "3", "6", "8", "9", "10"}:
            # List all members to choose from
            index_map = list_members()
            try:
                selected = int(input("Enter the number corresponding to the person: ").strip())
                if selected in index_map:
                    name = index_map[selected]

                    if choice == "1":  # Immediate family
                        person = family_tree.members[name]
                        family = person.get_person_family()
                        print(f"\nImmediate Family of {name}:")
                        for relation, names in family.items():
                            print(f"{relation}: {', '.join(names)}")

                    elif choice == "2":  # Cousins with parents
                        person = family_tree.members[name]
                        cousins = person.get_cousins_with_parents()
                        print(f"\nCousins of {name} with Parents and Spouses:")
                        print("\n".join(cousins))

                    elif choice == "3":  # Birthday
                        print(f"\n{name}'s Birthday: {family_tree.members[name].get_birthday()}")

                    elif choice == "6":  # Number of children
                        count = family_tree.get_children_count(name)
                        print(f"\n{name} has {count} children.")

                    elif choice == "8":  # Parent's name
                        person = family_tree.members[name]
                        parents = person.parents
                        if parents:
                            parent_names = [parent.name for parent in parents]
                            print(f"\n{name}'s Parent(s): {', '.join(parent_names)}")
                        else:
                            print(f"\n{name} has no known parents.")

                    elif choice == "9":  # Siblings
                        person = family_tree.members[name]
                        siblings = person.siblings
                        if siblings:
                            sibling_names = [sibling.name for sibling in siblings]
                            print(f"\n{name}'s Siblings: {', '.join(sibling_names)}")
                        else:
                            print(f"\n{name} has no known siblings.")

                    elif choice == "10":  # Grandchildren
                        person = family_tree.members[name]
                        grandchildren = []
                        for child in person.children:
                            for grandchild in child.children:
                                grandchildren.append(grandchild.name)
                        if grandchildren:
                            print(f"\n{name}'s Grandchildren: {', '.join(grandchildren)}")
                        else:
                            print(f"\n{name} has no known grandchildren.")

                else:
                    print("Invalid selection.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            family_tree.display_birthday_calendar()

        elif choice == "5":
            avg_age = family_tree.calculate_average_age_at_death()
            print(f"Average age at death: {avg_age:.2f}" if avg_age else "No deceased members found.")

        elif choice == "7":
            avg_children = family_tree.calculate_average_children_per_person()
            print(f"Average number of children per person: {avg_children:.2f}")

        elif choice == "11":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")