import zipfile
from tqdm import tqdm
import os
import shutil


class Backup_maker():
    def __init__(self):
        pass

    def makezip(self, folder_dir, directory, backup_name):
        # define the compression level
        try:
            import lzma
            compression = zipfile.ZIP_LZMA
        except:
            compression = zipfile.ZIP_STORED

        # create the zip
        zip = zipfile.ZipFile(backup_name + '.zip', 'w',
                              compression=compression)

        # get the files
        file_list = list()
        for root, dirs, files in os.walk(folder_dir):
            for file in files:
                file_list.append(file)

        # get the length of the root
        dir_length = len(folder_dir)

        t = tqdm(total=len(file_list), desc='Zipping files', position=0)
        descr = tqdm(total=0, desc='File...', bar_format='{desc}', position=1)
        n = 0

        try:
            # add the files
            for root, dirs, files in os.walk(folder_dir, topdown=True):
                for name in files:
                    # print(name)
                    descr.set_description_str(f'Current file: {name}')
                    zip.write(
                        root + '\\' + name, arcname=root[dir_length:] + '\\' + name, compress_type=compression)
                    n += 1
                    t.update()
        finally:
            t.close()
            descr.close()
            zip.close()

    def copyBackup(self, folder_dir, directory, backup_name):
        # show a nice progress bar
        t = tqdm(total=1, desc='Making a backup')
        # make a copy
        shutil.copytree(folder_dir, backup_name)
        t.update()
        t.close()
