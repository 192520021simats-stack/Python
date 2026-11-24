import csv
import re
from pathlib import Path


# College Fest Registration System
# Task 6 - Design Challenge


class InvalidRecord(Exception):
    pass


# Email validation
def valid_email(email):
    email = email.strip()

    if email.count("@") != 1:
        return False

    local, domain = email.split("@")

    return (
        bool(local)
        and bool(domain)
        and "." in domain
        and not any(ch.isspace() for ch in email)
        and not domain.startswith(".")
        and not domain.endswith(".")
    )


# Validate registration records
def validate(line):
    parts = line.strip().split(",", 4)

    if len(parts) != 5:
        raise InvalidRecord("Incorrect number of fields")

    reg, name, dept, email, events = map(str.strip, parts)

    if not all([reg, name, dept, email, events]):
        raise InvalidRecord("Missing required field")

    if not valid_email(email):
        raise InvalidRecord("Invalid email address")

    event_list = [e.strip() for e in events.split(";")]

    if not event_list or any(not e for e in event_list):
        raise InvalidRecord("Invalid event list")

    return {
        "reg": reg,
        "name": name,
        "dept": dept,
        "email": email,
        "events": event_list
    }


# Read department files
def read_department(path):
    with open(path, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            yield line_no, line


# Generate output reports
def write_reports(records, event_data, errors, output_dir):

    output_dir.mkdir(parents=True, exist_ok=True)

    # Master registration list
    with open(
        output_dir / "master_list.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Register Number",
            "Name",
            "Department",
            "Email",
            "Events"
        ])

        for r in records:
            writer.writerow([
                r["reg"],
                r["name"],
                r["dept"],
                r["email"],
                ";".join(r["events"])
            ])

    # Event-wise participant lists
    for event, students in event_data.items():

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            event
        )

        with open(
            output_dir / f"event_{safe_name}.txt",
            "w",
            encoding="utf-8"
        ) as f:

            for student in students:
                f.write(
                    f'{student["reg"]}, {student["name"]}\n'
                )

    # Summary report
    with open(
        output_dir / "summary.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("COLLEGE FEST SUMMARY\n")
        f.write(
            f"Total valid registrations: {len(records)}\n"
        )
        f.write(
            f"Total events: {len(event_data)}\n"
        )

        for event, students in event_data.items():
            f.write(
                f"{event}: {len(students)} participants\n"
            )

    # Error log
    with open(
        output_dir / "error.log",
        "w",
        encoding="utf-8"
    ) as f:

        for error in errors:
            f.write(error + "\n")


# Process all department files
def process(input_dir, output_dir):

    departments = ["CSE", "ECE", "EEE", "MECH", "CIVIL"]

    seen = set()
    records = []
    event_data = {}
    errors = []

    for dept in departments:

        path = Path(input_dir) / f"{dept}.txt"

        try:
            for line_no, line in read_department(path):

                if not line.strip():
                    continue

                try:
                    student = validate(line)

                    if student["reg"] in seen:
                        raise InvalidRecord(
                            "Duplicate registration"
                        )

                    seen.add(student["reg"])
                    records.append(student)

                    for event in student["events"]:
                        event_data.setdefault(event, [])
                        event_data[event].append(student)

                except InvalidRecord as e:
                    errors.append(
                        f"{path.name}, Line {line_no}: {e}"
                    )

        except FileNotFoundError:
            errors.append(
                f"Missing department file: {path.name}"
            )

        except PermissionError:
            errors.append(
                f"Permission denied: {path.name}"
            )

        except UnicodeDecodeError:
            errors.append(
                f"Wrong encoding: {path.name}"
            )

        except OSError as e:
            errors.append(
                f"File error in {path.name}: {e}"
            )

    write_reports(
        records,
        event_data,
        errors,
        Path(output_dir)
    )

    print("Processing completed.")
    print("Valid registrations:", len(records))
    print("Errors found:", len(errors))


# Create sample input files
def create_test_files():

    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)

    test_data = {
        "CSE.txt": (
            "192311001,Amrutha,CSE,amrutha@gmail.com,Music;Dance\n"
            "192311002,Bhavya,CSE,bhavya@gmail.com,Quiz;Dance\n"
        ),

        "ECE.txt": (
            "192311001,Amrutha,ECE,amrutha@gmail.com,Music\n"
            "192311003,Nethra,ECE,nethra@gmail.com,Quiz\n"
        ),

        "EEE.txt": (
            "192311004,Kavya,EEE,kavyaemail.com,Music\n"
            "192311005,Divya,EEE,divya@gmail.com,Dance\n"
        ),

        "MECH.txt": (
            "192311006,Harsha,MECH,harsha@gmail.com,Quiz\n"
            "192311007,MECH\n"
        )
    }

    for filename, data in test_data.items():
        (input_dir / filename).write_text(
            data,
            encoding="utf-8"
        )


# Main program
if __name__ == "__main__":

    create_test_files()

    process("input", "output")
