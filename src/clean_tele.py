import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

def is_mobile_number(mobile):
    if mobile.startswith('+84'):
        mobile = mobile[3:]
    elif mobile.startswith('84'):
        mobile = mobile[2:]
    return mobile.isdigit() and len(mobile) == 9

def is_folder(dir_folder):
    return os.path.isdir(f'{dir_folder}')

def is_skip_folder(folder):
    skip_delete_name = [
        'tdata', '2FA'
    ]
    if folder in skip_delete_name:
        return True

    # skip txt and session file
    if folder.endswith('.txt') or folder.endswith('.session'):
        return True

    return False

def cleanup_tdata(folder):
    listdir = os.listdir(f'{folder}/tdata')
    list_dir_only = [f'{folder}/tdata/{d}' for d in listdir if is_folder(f'{folder}/tdata/{d}')]
    for file in listdir:
        file_dir = f'{folder}/tdata/{file}'
        if is_folder(file_dir) and f'{file}s' in listdir:
            print(f'skip {file_dir}')
        elif not is_folder(file_dir) and 's' == file[-1] and f'{folder}/tdata/{file[:-1]}' in list_dir_only:
            print(f'skip {file_dir}')
        elif file in ['key_datas']:
            print(f'skip {file_dir}')
        else:
            print(f'deleting {file_dir}')
            remove_folder(file_dir)


def cleanup(mobile_folder):
    for file in os.listdir(mobile_folder):
        if not is_skip_folder(file):
            print(f'deleting file or folder {file}')
            remove_folder(f'{mobile_folder}/{file}')

    cleanup_tdata(mobile_folder)

def remove_folder(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def main(dir_tele):
    list_folder_tele = os.listdir(dir_tele)
    for folder in list_folder_tele:
        # check is folder and mobile format
        if is_folder(f'{dir_tele}/{folder}') and is_mobile_number(folder):
            cleanup(f'{dir_tele}/{folder}')

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    total_size = total_size / 1024 / 1024
    return total_size

if __name__ == '__main__':
    dir_mother = f"D:/tele/teleacc"
    list_folder = os.listdir(dir_mother)
    before_clean_folder = get_directory_size(f'{dir_mother}')
    for d in list_folder:
        dir_tele_data = f'{dir_mother}/{d}'
        if is_folder(dir_tele_data):
            main(dir_tele_data)
    after_clean_folder = get_directory_size(f'{dir_mother}')
    print(f'Before clean {before_clean_folder} | After clean {after_clean_folder}')