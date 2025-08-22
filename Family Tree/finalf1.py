class Person:
    def __init__(self, name, birth_date, death_date=None):
        """Initialize a Person object with a name, birthdate, and optional death date."""
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.parents = []
        self.children = []
        self.spouse = None

    def add_parent(self, parent):
        """Add a parent to this person."""
        if parent not in self.parents:
            self.parents.append(parent)
            parent.children.append(self)

    def get_parents(self):
        """Return the names of this person's parents."""
        return [parent.name for parent in self.parents] if self.parents else None

    def get_grandparents(self):
        """Return the names of this person's grandparents."""
        grandparents = []
        for parent in self.parents:
            grandparents.extend(parent.parents)
        return [grandparent.name for grandparent in grandparents] if grandparents else None

    def get_grandchildren(self):
        """Return the grandchildren of this person."""
        grandchildren = []
        for child in self.children:
            grandchildren.extend(child.children)
        return [grandchild.name for grandchild in grandchildren] if grandchildren else None

    def set_spouse(self, spouse):
        """Set the spouse for this person."""
        if self.spouse is None and spouse.spouse is None:
            self.spouse = spouse
            spouse.spouse = self

    def is_alive(self):
        """Check if the person is alive."""
        return self.death_date is None

    def get_siblings(self):
        """Return the siblings of this person."""
        siblings = set()
        for parent in self.parents:
            siblings.update(parent.children)
        siblings.discard(self)
        return [sibling.name for sibling in siblings] if siblings else None

    def get_immediate_family(self):
        """Return the immediate family of this person (parents, siblings, spouse, and children)."""
        return {
            "Parents": self.get_parents(),
            "Siblings": self.get_siblings(),
            "Spouse": [self.spouse.name if self.spouse else None],
            "Children": [child.name for child in self.children] if self.children else None,
        }

    def __str__(self):
        """Return a string representation of the person."""
        return f"{self.name} (Born: {self.birth_date}, Died: {self.death_date if self.death_date else 'Alive'})"


class FamilyTree:
    def __init__(self):
        """Initialize the family tree."""
        self.members = {}

    def add_member(self, name, birth_date, death_date=None):
        """Add a new family member."""
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
        """Set spouse relationships between two members."""
        if name1 in self.members and name2 in self.members:
            person1 = self.members[name1]
            person2 = self.members[name2]
            person1.set_spouse(person2)

    def get_parents(self, name):
        """Return the parents of a specific Person."""
        if name in self.members:
            return self.members[name].get_parents()
        return None

    def get_grandchildren(self, name):
        """Return the grandchildren of a specific Person."""
        if name in self.members:
            return self.members[name].get_grandchildren()
        return None


    def get_extended_family(self, name):
        """Get extended family categorized by type of relationship."""
        if name in self.members:
            person = self.members[name]

            # Start with immediate family
            extended_family = person.get_immediate_family()

            # Add additional categories
            extended_family.update({
                "Aunts and Uncles": [],
                "Cousins": [],
                "Grandchildren": person.get_grandchildren() or ["No grandchildren found"],
            })

            # Process aunts, uncles, and cousins
            for parent in person.parents:
                for sibling in parent.children:
                    if sibling != person:
                        extended_family["Aunts and Uncles"].append(sibling.name)
                        # Add cousins (children of aunts and uncles)
                        for cousin in sibling.children:
                            extended_family["Cousins"].append(cousin.name)

            # Remove duplicates and format output
            extended_family["Aunts and Uncles"] = (
                    list(set(extended_family["Aunts and Uncles"])) or ["No aunts and uncles found"]
            )
            extended_family["Cousins"] = (
                    list(set(extended_family["Cousins"])) or ["No cousins found"]
            )

            return extended_family

        return None

    @staticmethod
    def format_list(data, empty_message="No data available"):
        """Format lists for display, replacing empty lists or None with a default message."""
        if not data:
            return empty_message
        return ", ".join(data)

# Interactive Menu
if __name__ == "__main__":
    family_tree = FamilyTree()

    # Adding family members
    family_tree.add_member("Ali", "1940-06-21", "2002-05-24")
    family_tree.add_member("Fatemeh", "1945-09-01")
    family_tree.add_member("Mohammad", "1970-11-09")
    family_tree.add_member("Maryam", "1975-04-30")
    family_tree.add_member("Reza", "2000-05-08")
    family_tree.add_member("Sara", "2001-07-15")
    family_tree.add_member("Iman", "2004-11-21")
    family_tree.add_member("Leila", "2014-07-01")
    family_tree.add_member("Irfan", "2003-04-22")
    family_tree.add_member("Mehran", "2005-12-08")
    family_tree.add_member("Qazi Eisa", "2009-01-01")

    # Establish relationships
    family_tree.add_relationship("Ali", "Mohammad")
    family_tree.add_relationship("Fatemeh", "Mohammad")
    family_tree.add_relationship("Mohammad", "Reza")
    family_tree.add_relationship("Maryam", "Reza")
    family_tree.add_relationship("Mohammad", "Sara")
    family_tree.add_relationship("Maryam", "Sara")
    family_tree.add_relationship("Mohammad", "Iman")
    family_tree.add_relationship("Maryam", "Iman")
    family_tree.add_relationship("Reza", "Irfan")
    family_tree.add_relationship("Reza", "Mehran")
    family_tree.add_relationship("Reza", "Qazi Eisa")


    # Set spouses
    family_tree.set_spouse("Ali", "Fatemeh")
    family_tree.set_spouse("Mohammad", "Maryam")
    family_tree.set_spouse("Reza", "Leila")

    # Interactive Menu
    while True:
        print("\n--- Family Information ---")
        print("Available family members:")
        for name in family_tree.members.keys():
            print(f"- {name}")

        selected_name = input("Select a family member by name (or type 'exit' to quit): ").strip()
        if selected_name.lower() == "exit":
            print("Exiting...")
            break

        if selected_name in family_tree.members:
            member = family_tree.members[selected_name]
            print(f"\n--- Information for {member.name} ---")
            print(f"Parents: {family_tree.format_list(member.get_parents(), 'No parents recorded')}")
            print(f"\nGrandchildren: {family_tree.format_list(member.get_grandchildren(), 'No grandchildren found')}")
            print("\nImmediate Family:")
            immediate_family = member.get_immediate_family()
            for key, value in immediate_family.items():
                print(f"  {key}: {family_tree.format_list(value, f'No {key.lower()} found')}")
            extended_family = family_tree.get_extended_family(selected_name)
            if extended_family:
                print("\nExtended Family:")
                for key, value in extended_family.items():
                    print(f"  {key}: {family_tree.format_list(value, f'No {key.lower()} found')}")
            print(f"\nStatus: {'Alive' if member.is_alive() else 'Deceased'}")
        else:
            print("Invalid name. Please try again.")
