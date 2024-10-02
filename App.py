import lib.BinFileOperation as bfo
from os import system
from numpy import asarray, isin, sort
from pandas import DataFrame

while True:
    print("1. Show all data")
    print("2. Show specific data")
    print("3. Insert data")
    print("4. Edit data")
    print("5. Delete data")
    print("6. Export report")
    print("7. Exit")
    print("Go to the main menu or cancel by Ctrl+C")
    try:
        choice = input("Enter your choice: ")
        match choice:
            case '1':   # Show all data
                print("1. Show all data (average of scores)")
                print("2. Show all data (latest 4 scores)")
                choice = input("(Display All) Enter your display formatting options: ")
                bfo.showAllData(choice)
            case '2':   # Show specific data
                print("1. ID")
                print("2. Name")
                print("3. Department")
                print("4. Average Score")
                print("5. Score")
                print("6. Salary")
                print("Ctrl+C to cancel or go to the main menu")
                col = input("(Display Specific) What do you want to search by? Choose 1-6: ")
                column_choice = ['ID', 'Name', 'Department', 'Average Score', 'Score', 'Salary'][int(col) - 1]
                if col == '1' or col == '5':
                    print("Please enter a single ID or multiple IDs to search.")
                    print("Example. [A single ID] Enter ID: 0001")
                    print("Example. [Multiple IDs] Enter ID: 0001 0002 0003")
                elif col == '2':
                    print("Please enter a single name or multiple names to search.")
                    print("Example. [A single name] Enter Name: John")
                    print("Example. [Multiple names] Enter Name: John Peter")
                elif col == '3':
                    print("Please enter a single department or multiple departments to search.")
                    print("Example. [A single department] Enter Department: Engineering")
                    print("Example. [Multiple departments] Enter Department: Engineering IT")
                if col in ['4', '6']:
                    print("1. [>] More than")
                    print("2. [>=] More than or equal to ")
                    print("3. [<] Less than")
                    print("4. [<=] Less than or equal to")
                    print("5. [=] Equal to")
                    print("Ctrl+C to cancel or go to the main menu")
                    choice = input(f"(Display Specific) Please enter your choice (1-5): ")
                    compare_choice = ['More than', 'More than or equal to', 'Less than', 'Less than or equal to', 'Equal to'][int(choice) - 1]
                    match choice:
                        case '5':
                            print(f"Please enter a single {column_choice} or multiple {column_choice}s to search.")
                            print(f"Example. [A single {column_choice}] Enter Name: 80")
                            print(f"Example. [Multiple {column_choice}s] Enter Name: 10 20")
                            list_search = input(f"(Display Specific) Enter value: ").strip().split()
                        case _:
                            list_search = input(f"(Display Specific) Enter Value for finding {column_choice} that is {compare_choice}: ").strip().split()
                    bfo.showSpecificData(col, list_search, choice)
                elif col == '5':
                    list_search = input(f"(Display Specific) Enter ID: ").strip().split()
                    bfo.showSpecificData(col, list_search)
                elif col in ['1', '2', '3']:
                    list_search = input(f"(Display Specific) Enter {column_choice}: ").strip().split()
                    bfo.showSpecificData(col, list_search)
                else:
                    print("Invalid choice. Please try again.")
            case '3':   # Insert data
                number_of_data = int(input("(Insert) Enter the number of employees: "))
                for i in range(number_of_data):
                    print(f"Input data {i + 1}/{number_of_data}")
                    id = input("(Insert) Enter the ID: ")
                    name = input("(Insert) Enter the Name: ")
                    department = input("(Insert) Enter the Department: ")
                    print(f"Please enter the score (max 4 value). \nExample, Enter the score: 80 90 100 95")
                    score = input("(Insert) Enter the Score:")
                    score = list(map(float, score.strip().split()))
                    salary = float(input("(Insert) Enter the Salary: "))
                    bfo.addData(id.strip(), name.strip(), department.strip(), score, salary)
            case '4':   # Edit data
                print("1. Name")
                print("2. Department")
                print("3. Score")
                print("4. Salary")
                print("Ctrl+C to cancel or go to the main menu")
                col = input("(Edit) Select the option you want to edit: ")
                column_choice = ['Name', 'Department', 'Score', 'Salary'][int(col) - 1]
                print("Please enter a single ID or multiple IDs to edit.")
                print("Example. [A single ID] Enter ID: 0001")
                print("Example. [Multiple IDs] Enter ID: 0001 0002 0003")
                multi_id = input("(Edit) Enter ID: ")
                multi_id = tuple(multi_id.strip().split())
                if len(multi_id) == 0:
                    print("ID not found can't edit data.")
                    input("Press Enter to continue...")
                    continue
                match column_choice:
                    case 'Name':
                        print(f"Please enter new name to edit. (Must be equal to the number of IDs)")
                        print("Example. Enter the new name for ID('001', '002'): John Peter")
                        new_name = input(f"(Edit) Enter the new name for ID{multi_id}: ")
                        new_name = tuple(new_name.strip().split())
                        bfo.editData(column_choice,multi_id,new_name)
                    case 'Department':
                        print(f"Please enter new department to edit. (Must be equal to the number of IDs)")
                        print("Example. Enter the new department for ID('001', '002'): John Peter")
                        new_department = input(f"(Edit) Enter the new department for ID{multi_id}: ")
                        new_department = tuple(new_department.strip().split())
                        bfo.editData(column_choice,multi_id,new_department)
                    case 'Score':
                        print("1. Add new score")
                        print("2. Edit existing score")
                        choice_edit_score = input("(Edit) Enter your choice: ")
                        all_user_data = bfo.readDataFromBinFile()
                        all_user_data = [(user_data[0],user_data[1] , f"[{', '.join(list(map(str, user_data[3])))}]") for user_data in all_user_data]
                        dtype = [('ID', 'U20'),             # 4-character string for ID
                                ('Name', 'U20'),           # 10-character string for Name
                                ('Score', 'U30')]
                        all_user_data_fltr = asarray(all_user_data, dtype=dtype)
                        data_fltr = all_user_data_fltr[isin(all_user_data_fltr['ID'], multi_id)]
                        sorted_data = sort(data_fltr, order='ID')
                        if len(sorted_data) == 0:
                            raise Exception("ID not found can't edit score.")
                        df_data_fltr = DataFrame(data=sorted_data)
                        print(df_data_fltr.to_string(index=False))
                        multi_new_score = []
                        match choice_edit_score:
                            case '1':
                                for id in multi_id:
                                    print(f"Please enter new score to edit. (Max 4 value)")
                                    print(f"Example. Enter the new score: 80 90 100 95")
                                    new_score = input(f"(Edit>Add new>ID{id}) Enter the new score: ")
                                    new_score = list(new_score.strip().split())
                                    if len(new_score) == 0:
                                        print(f"Score not found can't edit score for {id}.")
                                        continue
                                    # while len(new_score) < 4:
                                    #     new_score.insert(0, 0)
                                    multi_new_score.append(new_score)
                                bfo.editData(column_choice,multi_id,multi_new_score,choice_edit_score)
                            case '2':
                                multi_index = []
                                all_user_data = bfo.readDataFromBinFile()
                                all_user_id = [user_data[0] for user_data in all_user_data]
                                for id in multi_id:
                                    if id not in all_user_id:
                                        print(f"ID {id} not found can't edit score for {id}.")
                                        continue
                                    print(f"Please enter the index of score to edit. (0-3)")
                                    print(f"Example. Enter the index: 0 1 2 3")
                                    index = input(f"(Edit>Edit existing>ID{id}) Enter the index: ")
                                    index = tuple(index.strip().split())
                                    if len(index) == 0:
                                        print(f"Index not found can't edit score for {id}.")
                                        continue
                                    multi_index.append(index)
                                    print(f"Please enter new score to edit. (According to position of idex)")
                                    print(f"Example. Enter the new score for index ('0', '2'): 80 90")
                                    new_score = input(f"(Edit>Edit existing>ID{id}) Enter the new score for index {index}: ")
                                    new_score = tuple(new_score.strip().split())
                                    if len(new_score) == 0:
                                        print(f"Score not found can't edit score for {id}.")
                                        continue
                                    elif len(new_score) != len(index):
                                        print(f"Score and index length not same can't edit score for {id}.")
                                        continue
                                    multi_new_score.append(new_score)
                                bfo.editData(column_choice,multi_id,multi_new_score,choice_edit_score, multi_index)
                            case _:
                                print("Invalid choice. Please try again.")
                    case 'Salary':
                        print("1. Add new salary")
                        print("2. Cut salary")
                        print("3. Edit existing salary")
                        choice_edit_salary = input("(Edit) Enter your choice: ")
                        match choice_edit_salary:
                            case '1':
                                print(f"Please enter value for add salary of ID {multi_id}.")
                                print("Example. Enter a single number for add salary: 1000")
                                try:
                                    new_salary = float(input("(Edit) Enter a single number for add salary: "))
                                except ValueError:
                                    print("Input 1 number only.")
                                else:
                                    bfo.editData(column_choice,multi_id, new_salary, choice_edit_salary)
                            case '2':
                                print(f"Please enter value for cut salary of ID {multi_id}.")
                                print("Example. Enter a single number for cut salary: 1000")
                                try:
                                    new_salary = float(input("(Edit) Enter a single number for cut salary: "))
                                except ValueError:
                                    print("Input 1 number only.")
                                else:
                                    bfo.editData(column_choice,multi_id, new_salary, choice_edit_salary)
                            case '3':
                                print(f"Please enter new salary for {multi_id}.")
                                print(f"Example. Enter a single number for new salary: 10000")
                                new_salary = input("(Edit) Enter a single number for new salary:")
                                new_salary = tuple(map(float, new_salary.strip().split()))
                                if len(new_salary) == 0:
                                    print(f"Salary not found can't edit salary for {multi_id}.")
                                elif len(new_salary) != len(multi_id):
                                    print(f"Salary and ID length not same can't edit salary for {multi_id}.")
                                else:
                                    bfo.editData(column_choice,multi_id, new_salary, choice_edit_salary)
                            case _:
                                raise Exception("Invalid choice. Please try again.")
                    case _:
                        print("Invalid choice. Please try again.")
            case '5':   # Delete data
                print("Please enter a single ID or multiple IDs to delete.")
                print("Example. [A single ID] Enter ID: 0001")
                print("Example. [Multiple IDs] Enter ID: 0001 0002 0003")
                list_search = input(f"(Delete) Enter ID:").strip().split()
                bfo.deleteData(list_search)
            case '6':   # Export report
                bfo.exportReport()
            case '7':   # Exit
                if input("Do you want to exit? (y/[n]): ").lower() == 'y':
                    break
            case _:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("Operation cancelled.")
    else:
        print("================ (End of operation) ================")
        input("Press Enter to continue...")
        print()
    # finally:
    #     system('cls')