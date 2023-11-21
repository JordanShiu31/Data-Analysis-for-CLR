import pandas as pd
import os
import os.path

# constants to covert to size
MB = 2
GB = 3

def find_main_folders(root):
    # next will only get the first results the form of a tuple (durpath,dirnames,filenames) and the [1] will return the dirnames
    headers = next(os.walk(root))[1]
    return [os.path.join(root, x) for x in headers]

def create_list_of_all_files_into_csv(root, folder_counter):
    df = pd.DataFrame(columns=["Filename", "Size (MB)", "File_type","Location"])
    i = 1
    # loops in order dirpath -> dirnames[1] -> filenames[1] etc
    for dirpath, dirnames, filenames in os.walk(root):
        for file in filenames:
            file_path = os.path.join(dirpath, file)

            # checks if the path is not a symbolic link
            if not os.path.islink(file_path):
                file_size = os.path.getsize(file_path)
                # converts to  MBs (GB would be 3)
                size = (file_size / 1024)**MB
                _, extension = os.path.splitext(file)

            # adds files into the dataframe
            df.loc[i, "Filename"] = file
            df.loc[i, "Size (MB)"] = round(size,2)
            df.loc[i, "File_type"] = extension
            df.loc[i, "Location"] = file_path

            # print(f"Filepath name is: {file} and size is: {size:.2f}")
            i+=1
        # df.loc[i] = df[["Size (MB)", "File_type"]].groupby(["File_type"]).aggregate(["sum","count"])
    new_df = df[["Size (MB)", "File_type"]].groupby(["File_type"]).aggregate(["sum","count"]).droplevel(0, axis=1)
    # new_df = df[["File_type", "Size (MB)"]].groupby("File_type").aggregate({'Unique file type':'count','Total Size':'sum','Total Count':'max'}).copy()
    # print(new_df)
    # print(new_df["sum"]) 
    print(df.join(new_df, lsuffix='_caller', rsuffix='_other'))
    # print(df)

    # df.to_csv(f"C:/Users/jordan.shiu/OneDrive - AECOM/Desktop/File Size App/test_{folder_counter}.csv")

# root = "C:/Users/jordan.shiu/OneDrive - AECOM//0. Working Folder - CLR2 TA - Movement Workstream"
root = "C:/Users/jordan.shiu/OneDrive - AECOM/Documents/Grad 2021/CLR/12_09_2022 Contruction Phase"
list_of_main_folders = find_main_folders(root)
folder_counter = 1
# create_list_of_all_files_into_csv(dir_path)
for folder_path in list_of_main_folders:
    if os.path.exists(folder_path):
        create_list_of_all_files_into_csv(folder_path, folder_counter)
    else:
        print(f"The file: {folder_path} does not exist")
    folder_counter +=1