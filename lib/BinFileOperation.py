import struct
import numpy as np
import pandas as pd

bin_path = "data.bin"

def readDataFromBinFile() -> list:
    list_records = []
    try:
        with open(bin_path, "rb") as file:
            record_size = struct.calcsize("20s20s20s20sf")
            while True:
                data = file.read(record_size)
                if not data:
                    break
                records = struct.unpack("20s20s20s20sf", data)
                record_3 = [float(score) for score in records[3].decode().strip('\x00').split()]
                if len(record_3) < 4:
                    record_3 += [0.0] * (4 - len(record_3))
                records = [records[0].decode().strip('\x00'), records[1].decode().strip(
                    '\x00'), records[2].decode().strip('\x00'), record_3, records[4]]
                list_records.append(records)
    except FileNotFoundError:
        with open(bin_path, "wb") as file:
            file.write(b'')
    return list_records


def writeDataToBinFile(list_records: list):
    if len(list_records) == 0:
        with open(bin_path, "wb") as file:
            file.write(b'')
    for index, record in enumerate(list_records):
        if index == 0:
            with open(bin_path, "wb") as file:
                data = struct.pack("20s20s20s20sf", record[0].encode(), record[1].encode(
                ), record[2].encode(), ' '.join(map(str, record[3])).encode(), record[4])
                file.write(data)
        else:
            with open(bin_path, "ab") as file:
                data = struct.pack("20s20s20s20sf", record[0].encode(), record[1].encode(
                ), record[2].encode(), ' '.join(map(str, record[3])).encode(), record[4])
                file.write(data)


def editData(pointed_col: str, id: tuple, new_data, choice_edit:str=None, selected_col:list=None):
    list_records = readDataFromBinFile()
    match pointed_col:
        case 'Name':
            for i in range(len(id)):
                for index, record in enumerate(list_records):
                    if record[0] == id[i]:
                        try:
                            list_records[index][1] = new_data[i]
                        except IndexError:
                            raise Exception(f"Input data is not enough for {id[i]}.(required: {len(id)}, got: {len(new_data)})")
        case 'Department':
            for i in range(len(id)):
                for index, record in enumerate(list_records):
                    if record[0] == id[i]:
                        try:
                            list_records[index][2] = new_data[i]
                        except IndexError:
                            list_records[index][2] = new_data[-1]
        case 'Score':
            match choice_edit:
                case '1':   # Add
                    for i in range(len(id)):
                        for index, record in enumerate(list_records):
                            if record[0] == id[i]:
                                for score in new_data[i]:
                                    list_records[index][3].append(score)
                                while len(list_records[index][3]) > 4:
                                    list_records[index][3].pop(0)
                                    # print(list_records[index][3])
                case '2':   # selective update
                    for i in range(len(id)):
                        for index, record in enumerate(list_records):
                            if record[0] == id[i]:
                                # print(record[0])
                                # print(selected_col[i])
                                for col in selected_col[i]:
                                    # print(list_records[index][3][int(col)])
                                    # print(new_data[i][selected_col[i].index(col)])
                                    list_records[index][3][int(col)] = new_data[i][selected_col[i].index(col)]
        case 'Salary':
            match choice_edit:
                case '1':
                    for i in range(len(id)):
                        for index, record in enumerate(list_records):
                            if record[0] == id[i]:
                                list_records[index][4] += new_data
                case '2':
                    for i in range(len(id)):
                        for index, record in enumerate(list_records):
                            if record[0] == id[i]:
                                list_records[index][4] -= new_data
                case '3':
                    for i in range(len(id)):
                        for index, record in enumerate(list_records):
                            if record[0] == id[i]:
                                list_records[index][4] = new_data[i]
        case _:
            print("Invalid choice. Please try again.")
            return
    writeDataToBinFile(list_records)

def addData(id: str, name: str, department: str, score: list, salary: float):
    try:
        list_records = readDataFromBinFile()
        for record in list_records:
            if record[0] == id:
                raise Exception(f"ID {id} already exists.")
        list_records.append([id, name, department, score, salary])
    except Exception as e:
        # list_records = [[id, name, department, score, salary]]
        print(e)
    else:
        print(f"ID {id} has been added successfully.")
        with open(bin_path, "ab") as file:
            data = struct.pack("20s20s20s20sf", id.encode(), name.encode(
            ), department.encode(), ' '.join(map(str, score)).encode(), salary)
            file.write(data)

def deleteData(multi_id: list):
    list_records = readDataFromBinFile()
    all_user_id = [user_data[0] for user_data in list_records]
    for id in multi_id:
        if id not in all_user_id:
            print(f"ID {id} not found.")
    list_index = []
    for index, record in enumerate(list_records):
        if record[0] in multi_id:
            list_index.append(index)
    list_index.sort(reverse=True)
    list_deleted = []
    for index in list_index:
        list_deleted.append(list_records.pop(index))
    writeDataToBinFile(list_records)
    for record in list_deleted:
        print(f"ID {record[0]} has been deleted successfully.")

def showAllData(choice=None):
    list_records = readDataFromBinFile()
    np.seterr(all='ignore')
    choice = choice
    match choice:
        case '1':
            list_records = [(record[0], record[1], record[2], np.mean(record[3]), record[4]) for record in list_records]
            # Define the data types for each field
            dtype = [('ID', 'U20'),             # 4-character string for ID
                     ('Name', 'U20'),           # 10-character string for Name
                     # 10-character string for Department
                     ('Department', 'U20'),
                     ('Average Score', 'f4'),   # float for Score
                     ('Salary', 'f4')]          # float for Salary
            # Create a structured NumPy array
            data_arr = np.asarray(list_records, dtype=dtype)
        case '2':
            list_records = [(record[0], record[1], record[2], ', '.join(
                list(map(str, record[3]))), record[4]) for record in list_records]
            # Define the data types for each field
            dtype = [('ID', 'U20'),             # 4-character string for ID
                     ('Name', 'U20'),           # 10-character string for Name
                     # 10-character string for Department
                     ('Department', 'U20'),
                     ('Score', 'U20'),
                     ('Salary', 'f4')]          # float for Salary
            # Create a structured NumPy array
            data_arr = np.asarray(list_records, dtype=dtype)
        case _:
            print("Invalid choice. Please try again.")
            return
    # Sort by the 'ID' field
    sorted_data = np.sort(data_arr, order='ID')
    # Convert to Pandas DataFrame for display
    df_data_arr = pd.DataFrame(sorted_data)
    # Display the data without the index column
    if df_data_arr.empty:
        print("Data not found.")
        return
    print(df_data_arr.to_string(index=False))


def showSpecificData(col: int, list_search=None, choice=None):
    list_records = readDataFromBinFile()
    col = ['ID', 'Name', 'Department', 'Average Score',
           'Score', 'Salary'][int(col) - 1]
    if col == 'Score':
        list_records = [(record[0], record[1], record[2], ','.join(
            list(map(str, record[3]))), record[4]) for record in list_records]
        # Define the data types for each field
        dtype = [('ID', 'U20'),             # 4-character string for ID
                 ('Name', 'U20'),           # 10-character string for Name
                 ('Department', 'U20'),     # 10-character string for Department
                 ('Score', 'U20'),
                 ('Salary', 'f4')]          # float for Salary
        # Create a structured NumPy array
        data_arr = np.asarray(list_records, dtype=dtype)
    else:
        list_records = [(record[0], record[1], record[2], np.mean(
            record[3]), record[4]) for record in list_records]
        # Define the data types for each field
        dtype = [('ID', 'U20'),             # 4-character string for ID
                 ('Name', 'U20'),           # 10-character string for Name
                 ('Department', 'U20'),     # 10-character string for Department
                 ('Average Score', 'f4'),   # float for Score
                 ('Salary', 'f4')]          # float for Salary
        # Create a structured NumPy array
        data_arr = np.asarray(list_records, dtype=dtype)
    if col == 'Average Score' or col == 'Salary':
        choice = choice
        match choice:
            case '1':
                data_fltr = data_arr[data_arr[col] > float(list_search[0])]
            case '2':
                data_fltr = data_arr[data_arr[col] >= float(list_search[0])]
            case '3':
                data_fltr = data_arr[data_arr[col] < float(list_search[0])]
            case '4':
                data_fltr = data_arr[data_arr[col] <= float(list_search[0])]
            case _:
                list_search = [float(score) for score in list_search]
                data_fltr = data_arr[np.isin(data_arr[col], list_search)]
        sorted_data = np.sort(data_fltr, order=col)
    elif col == 'ID' or col == 'Name':
        data_fltr = data_arr[np.isin(data_arr[col], list_search)]
        sorted_data = np.sort(data_fltr, order='ID')
    elif col == 'Department':
        data_fltr = data_arr[np.isin(data_arr[col], list_search)]
        sorted_data = np.sort(data_fltr, order='Department')
    elif col == 'Score':
        data_fltr = data_arr[np.isin(data_arr['ID'], list_search)]
        sorted_data = np.sort(data_fltr, order='ID')
    df_data_fltr = pd.DataFrame(data=sorted_data)
    if df_data_fltr.empty:
        print("No data found.")
        return
    print(df_data_fltr.to_string(index=False))


def exportReport():
    data_bin_file = np.array(readDataFromBinFile(), dtype="object")
    # จัดกลุ่มตามแผนก
    departments = {}
    for record in data_bin_file:
        emp_id, name, dept, scores, salary = record
        avg_score = sum(scores) / len(scores)
        if dept not in departments:
            departments[dept] = {
                'employees': [], 'total_score': 0.0, 'count': 0, 'top_performer': (None, 0)}

        departments[dept]['employees'].append((name, avg_score))
        departments[dept]['total_score'] += avg_score
        departments[dept]['count'] += 1

        # อัปเดตผู้ทำคะแนนสูงสุด
        if avg_score > departments[dept]['top_performer'][1]:
            departments[dept]['top_performer'] = (name, avg_score)

    # คำนวณและพิมพ์รายงาน
    best_department = (None, 0)
    str_report = ""
    str_report += "Summary Report:\n"

    for dept, info in departments.items():
        avg_dept_score = info['total_score'] / info['count']
        str_report += f"Department: {dept}\n"

        for name, avg_score in info['employees']:
            str_report += f"  {name}: Average Score = {avg_score:.2f}\n"

        top_performer, top_score = info['top_performer']
        str_report += f"Top Performer: {
            top_performer} Average score = {top_score:.2f}\n"

        # หาว่าแผนกไหนมีคะแนนเฉลี่ยสูงสุด
        if avg_dept_score > best_department[1]:
            best_department = (dept, avg_dept_score)

    str_report += f"\nBest Department: {
        best_department[0]} Average score = {best_department[1]:.2f}\n"

    with open("report.txt", "w") as file:
        file.write(str_report)
    print("Report exported to report.txt successfully.")


def main():
    # showSpecificData(1, ['0001', '0002', '0003'])
    # editData(1, ['0001', '0002', '0003'], ['Silfy', 'Vyne', 'Buck'])
    # editData("Score", ['0001', '0002', '0003'], [[97, 98, 99], [
    #          45, 46, 47], [50, 60, 70]], '2', [['1', '3', '2'], ['1', '2', '3'], ['3', '2', '1']])
    # editData(4, ['0001', '0002', '0003'], [10000, 20000, 30000], '3')
    # showSpecificData(5, ['0001', '0002', '0003'])
    # addData('0001', 'Silfy', 'IT', [97, 98, 99], 10000)
    # addData('0002', 'Silfy', 'IT', [97, 98, 99], 10000)
    # showAllData('1')
    # deleteData(['0001', '0002', '0003'])
    pass


main()
