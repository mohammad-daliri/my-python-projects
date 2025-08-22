from collections import defaultdict
from datetime import datetime

class Person:
    def __init__(self, name, birth_date, death_date=None):
        self.name = name  # The person's name
        self.birth_date = birth_date  # The person's birthday
        self.death_date = death_date  # The date of death (if known)
        self.parents = []  # List to store parents
        self.siblings = []  # List to store siblings
        self.children = []  # List to store children
        self.spouse = None  # Store spouse

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
            if self not in parent.children:
                parent.children.append(self)

            # Automatically add siblings from the parent's children
            for sibling in parent.children:
                if sibling is not self and sibling not in self.siblings:
                    self.add_sibling(sibling)

    def add_sibling(self, sibling):
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            if self not in sibling.siblings:
                sibling.siblings.append(self)

    def set_spouse(self, spouse):
        if self.spouse is None:
            self.spouse = spouse
            spouse.spouse = self

    def get_person_family(self):
        immediate_family = {
            "Parents": [parent.name for parent in self.parents] if self.parents else ["No parents"],
            "Siblings": [sibling.name for sibling in self.siblings] if self.siblings else ["No siblings"],
            "Spouse": self.spouse.name if self.spouse else "No spouse",
            "Children": [child.name for child in self.children] if self.children else ["No children"],
        }
        return immediate_family

    def get_cousins_with_parents(self):
        cousins_with_parents = []
        for parent in self.parents:
            for aunt_uncle in parent.siblings:
                # Include the spouse of the aunt/uncle
                spouse_name = f" & {aunt_uncle.spouse.name}" if aunt_uncle.spouse else ""
                for cousin in aunt_uncle.children:
                    cousins_with_parents.append(f"{cousin.name} (Parent: {aunt_uncle.name}{spouse_name})")
        return cousins_with_parents if cousins_with_parents else ["No cousins found"]

    def get_birthday(self):
        return f"{self.name}: {self.birth_date}"


def get_birthday_calendar(family_members):
    calendar = defaultdict(list)
    for member in family_members.values():
        # Extract month and day in MM-DD format
        birth_month_day = datetime.strptime(member.birth_date, "%Y-%m-%d").strftime("%m-%d")
        calendar[birth_month_day].append(member.name)

    print("\nBirthday Calendar:")
    for date, members in sorted(calendar.items()):
        print(f"[{date}]: {', '.join(members)}")


if __name__ == "__main__":
    # Create family members
    hamza = Person("Hamza", "1940-12-21")  # Grandfather
    bibi_gul = Person("Bibi Gul", "1945-07-09")  # Grandmother

    asad = Person("Asad", "1970-04-06")  # Father
    zainab = Person("Zainab", "1975-09-04")  # Mother
    khan = Person("Khan", "1968-09-17")  # Uncle
    samina = Person("Samina", "1980-06-01")  # Aunt

    ali = Person("Ali", "2000-04-07")  # Son
    aisha = Person("Aisha", "2003-05-04")  # Daughter
    bilal = Person("Bilal", "2005-03-19")  # Son

    saif = Person("Saif", "1998-07-01")  # Cousin (Khan's son)
    sadia = Person("Sadia", "2002-11-01")  # Cousin (Khan's daughter)
    omer = Person("Omer", "2007-01-01")  # Cousin (Khan's son)

    fatima = Person("Fatima", "2025-02-01")
  # Granddaughter (Aisha's child)
    hassan = Person("Hassan", "2000-10-10")  # Aisha's spouse

    ahmad = Person("Ahmad", "1973-03-15")  # Distant uncle (Hamza's younger brother)
    shabana = Person("Shabana", "1978-08-22")  # Ahmad's wife
    nida = Person("Nida", "2001-02-18")  # Ahmad and Shabana's daughter

    # Build relationships
    hamza.set_spouse(bibi_gul)
    asad.add_parent(hamza)
    asad.add_parent(bibi_gul)
    khan.add_parent(hamza)
    khan.add_parent(bibi_gul)
    ahmad.add_parent(hamza)
    ahmad.add_parent(bibi_gul)

    asad.set_spouse(zainab)
    ali.add_parent(asad)
    ali.add_parent(zainab)

    aisha.add_parent(asad)
    aisha.add_parent(zainab)

    bilal.add_parent(asad)
    bilal.add_parent(zainab)

    aisha.set_spouse(hassan)
    fatima.add_parent(aisha)
    fatima.add_parent(hassan)

    khan.set_spouse(samina)
    saif.add_parent(khan)
    saif.add_parent(samina)

    sadia.add_parent(khan)
    sadia.add_parent(samina)

    omer.add_parent(khan)
    omer.add_parent(samina)

    ahmad.set_spouse(shabana)
    nida.add_parent(ahmad)
    nida.add_parent(shabana)

    # Store family members in a dictionary for dynamic selection
    family_members = {
        person.name: person for person in [
            hamza, bibi_gul, asad, zainab, ali, aisha, bilal, fatima, hassan,
            khan, samina, saif, sadia, omer, ahmad, shabana, nida
        ]
    }

    # Menu for user interaction
    while True:
        print("\n--- Family Tree Features ---")
        print("1: View Siblings")
        print("2: View Cousins with Parents")
        print("3: View Birthday of Selected Individual")
        print("4: View Family Birthday Calendar")
        print("5: Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            selected_name = input("Enter the person's name to view siblings: ").strip()
            if selected_name in family_members:
                member = family_members[selected_name]
                siblings = member.get_person_family()["Siblings"]
                print(f"Siblings of {member.name}: {', '.join(siblings)}")
            else:
                print("Invalid name. Try again.")

        elif choice == "2":
            selected_name = input("Enter the person's name to view cousins: ").strip()
            if selected_name in family_members:
                member = family_members[selected_name]
                cousins = member.get_cousins_with_parents()
                print("\nCousins with Parents and Their Spouses:")
                print("\n".join(cousins))
            else:
                print("Invalid name. Try again.")

        elif choice == "3":
            selected_name = input("Enter the person's name to view their birthday: ").strip()
            if selected_name in family_members:
                print(f"{family_members[selected_name].get_birthday()}")
            else:
                print("Invalid name. Try again.")

        elif choice == "4":
            get_birthday_calendar(family_members)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")
