import os
import shutil
from tqdm import tqdm
import csv
from tablemaker.tablemaker import StandardTable

class Shortcutter():
    def __init__(self):
        pass

    def loadShortcuts(self):
        file = open('C:\\Users\\Nutzer\\Desktop\\Private\\Programming\\Python\\CLI\\backup\\backup_pkg\\data\\shortcuts.csv')
        reader = csv.reader(file)
        shortcut_data = list(reader)

        # remove the header
        del shortcut_data[0]

        return shortcut_data

    def evaluateShortcut(self, shortcut):
        shortcut_data = self.loadShortcuts()

        for command in shortcut_data:
            if shortcut == command[0]:
                return command[1], command[2], command[3], command[4]

        exit(1)

    def addShortcut(self, shortcut, backup_type, folder, directory, name):

        # check if a shortcut already exists
        shortcuts = self.loadShortcuts()
        # get all the shortcut names
        shortcut_names = list()
        for short in shortcuts:
            shortcut_names.append(short[0])
        # write the shortcut
        if not shortcut in shortcut_names:
            with open('C:\\Users\\Nutzer\\Desktop\\Private\\Programming\\Python\\CLI\\backup\\backup_pkg\\data\\shortcuts.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['shortcut', 'type', 'folder', 'directory', 'name'])
                for short in shortcuts:
                    writer.writerow(short)
                writer.writerow([shortcut, backup_type, folder, directory, name])
            return True
        else:
            return False

    def listShortcuts(self):
        shortcuts = self.loadShortcuts()

        # put all the commands and the corresponding shortcuts into a list
        shortcuts = self.loadShortcuts()
        for shortcut in shortcuts:
            shortcut.insert(1, 'backup make')
            shortcut.insert(3, '-f')
            shortcut.insert(5, '-d')
            shortcut.insert(7, '-n')

        # convert everything to a table
        table = StandardTable()
        table.header_items = ['shortcut', 'command:', 'type', '', 'folder', '', 'directory', '', 'name']
        table.addRows(shortcuts)

        return table.get()