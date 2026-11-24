import time
import random
import string


# Normalise phone numbers
def normalise_phone(phone):
    digits = "".join(ch for ch in phone if ch.isdigit())

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits


# Normalise names
def normalise_name(name):
    return " ".join(name.casefold().split())


# Normalise emails
def normalise_email(email):
    return email.strip().casefold()


# Union-Find data structure
class UnionFind:

    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            self.parent[root_b] = root_a


# Contact merging function
def merge_contacts(contacts):

    uf = UnionFind()
    processed = []

    for contact in contacts:

        name = contact.get("name", "").strip()

        phones = {
            normalise_phone(p)
            for p in contact.get("phones", [])
            if normalise_phone(p)
        }

        emails = {
            normalise_email(e)
            for e in contact.get("emails", [])
            if normalise_email(e)
        }

        processed.append({
            "name": name,
            "phones": phones,
            "emails": emails
        })

        identifiers = (
            {"P:" + p for p in phones}
            | {"E:" + e for e in emails}
        )

        identifiers = list(identifiers)

        if identifiers:
            first = identifiers[0]

            for identifier in identifiers[1:]:
                uf.union(first, identifier)

    # Combine contacts into groups
    merged = {}

    for contact in processed:

        identifiers = (
            {"P:" + p for p in contact["phones"]}
            | {"E:" + e for e in contact["emails"]}
        )

        if identifiers:
            root = uf.find(next(iter(identifiers)))
        else:
            root = "EMPTY:" + str(id(contact))

        if root not in merged:
            merged[root] = {
                "names": set(),
                "phones": set(),
                "emails": set()
            }

        if contact["name"]:
            merged[root]["names"].add(contact["name"])

        merged[root]["phones"].update(contact["phones"])
        merged[root]["emails"].update(contact["emails"])

    return list(merged.values())


# Sample contacts from three sources
contacts = [
    {
        "name": "Dr. Ravi",
        "phones": ["+91 98400 12345"],
        "emails": ["ravi@gmail.com"]
    },
    {
        "name": "ravi kumar",
        "phones": ["9840012345"],
        "emails": ["ravi.kumar@gmail.com"]
    },
    {
        "name": "Anu",
        "phones": ["9876543210"],
        "emails": ["anu@gmail.com"]
    },
    {
        "name": "Anu",
        "phones": ["+91-98765-43210"],
        "emails": ["ANU@gmail.com"]
    },
    {
        "name": "Kumar",
        "phones": [],
        "emails": ["kumar@gmail.com"]
    },
    {
        "name": "Ravi",
        "phones": [],
        "emails": []
    }
]


# Merge contacts
result = merge_contacts(contacts)

print("Merged Contacts:")

for contact in result:
    print("\nNames:", sorted(contact["names"]))
    print("Phone Numbers:", sorted(contact["phones"]))
    print("Emails:", sorted(contact["emails"]))


# Testing phone formats
print("\nPhone Normalisation:")
print(normalise_phone("+91 98400 12345"))
print(normalise_phone("9840012345"))


# Testing two different people with the same name
same_name_contacts = [
    {
        "name": "Ravi",
        "phones": ["9000000001"],
        "emails": []
    },
    {
        "name": "Ravi",
        "phones": ["9000000002"],
        "emails": []
    }
]

print("\nSame Name Test:")
print(merge_contacts(same_name_contacts))


# Experimental investigation
def generate_contacts(size):
    data = []

    for i in range(size):
        data.append({
            "name": "Person" + str(i),
            "phones": ["9" + str(100000000 + i)],
            "emails": ["person" + str(i) + "@gmail.com"]
        })

    return data


for size in [1000, 100000]:

    data = generate_contacts(size)

    start = time.perf_counter()

    merged = merge_contacts(data)

    execution_time = time.perf_counter() - start

    print("\nContacts:", size)
    print("Merged records:", len(merged))
    print("Execution time:", execution_time)
