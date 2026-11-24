import re


def first_k_summary(text, k=2):
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip()
    )

    sentences = [
        s for s in sentences if s
    ]

    return " ".join(sentences[:k])


complaint = (
    "The road is dirty. "
    "Smoke is coming from the factory. "
    "The drainage system is broken. "
    "Immediate action is required."
)

print("Original Complaint:")
print(complaint)

print("\nFirst K Summary:")
print(first_k_summary(complaint, 2))
