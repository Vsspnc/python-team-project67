import struct


if __name__ == "__main__":
    pathFile = "data.bin"

    list_records = [
        # data employee
        ("0001", "Robert", "Engineering",
         "92 93 90 91", 40000),
        ("0002", "Alice", "Sales", "80 81 75 79", 25000),
        ("0003", "John", "Marketing", "85 80 82 81", 35000),
        ("0004", "Emily", "Finance", "95 95 95 96", 45000),
        ("0005", "David", "HR", "95 95 95 96", 30000),
        ("0008", "Jessica", "Marketing", "85 80 82 81", 38000),
        ("0009", "Daniel", "Finance", "80 81 75 79", 47000),
        ("0010", "Sophia", "HR", "95 95 95 96", 28000),
        ("0011", "Matthew", "Engineering", "80 81 75 79", 41000),
        ("0012", "Emma", "Sales", "92 93 90 91", 27000),
        ("0013", "Andrew", "Marketing", "95 95 95 96", 36000),
        ("0014", "Olivia", "Finance", "92 93 90 91", 48000),
        ("0015", "James", "HR", "85 80 82 81", 32000),
        ("0006", "Sarah", "Engineering", "95 95 95 96", 42000),
        ("0007", "Michael", "Sales", "80 81 75 79", 23000),
    ]
    for index, record in enumerate(list_records):
        if index == 0:
            with open(pathFile, "wb") as file:
                data = struct.pack("20s20s20s20sf", record[0].encode(), record[1].encode(
                ), record[2].encode(), record[3].encode(), record[4])
                file.write(data)
        else:
            with open(pathFile, "ab") as file:
                data = struct.pack("20s20s20s20sf", record[0].encode(), record[1].encode(
                ), record[2].encode(), record[3].encode(), record[4])
                file.write(data)
