import os
def clear_media_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)

            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(e)
        pass