# a simple programme to make a backup of a file
from backup_pkg.shortcutter import Shortcutter
from backup_pkg.backup_maker import Backup_maker
import click
from tablemaker.tablemaker import StandardTable
print('\n')
# from zipfile_infolist import print_info

bm = Backup_maker()
short = Shortcutter()


@click.group()
def main():
    pass

#
# Create a backup with a full command
#


@main.command()
# which type of backup
@click.option('--zip', '-z', 'backup_type', flag_value='zip', default=True, help='save the backup as a zip')
@click.option('--normal', '-nl', 'backup_type', flag_value='normal', help='save a backup as a copy of the folder')
# define the folder to backup, the directory to save it in and the name
@click.option('--folder', '-f', default='default', type=str, help='defines the folder to backup')
@click.option('--directory', '-d', default='C:\\Users\\Nutzer\\Desktop', type=str, help='the directory to save the backup in')
@click.option('--name', '-n', default='default', type=str, help='define the name of the backup')
def make(backup_type, folder, directory, name):
    '''Make a backup'''
    if folder == 'default':
        click.echo(f'Error: Missing Option "folder" / "-f".')
        return

    # get the folder dir
    folder = resolveDirectory(folder)

    # resolve the directory
    directory = resolveDirectory(directory)

    # get the backup name
    name = makeName(name, folder, directory)

    if backup_type == 'zip' or backup_type == '--zip' or backup_type == '-z':
        # zip and save
        bm.makezip(folder, directory, name)
        click.echo(f'Final directory: {name}')
        click.echo('Successfully made a backup')

    elif backup_type == 'normal' or backup_type == '--normal' or backup_type == '-nl':
        # make the backup and save
        bm.copyBackup(folder, directory, name)
        click.echo(f'Final directory: {name}')
        click.echo('Successfully made a backup')

#
# Save and load shortcuts (summarize a command to a single word)
#


@main.command()
@click.option('--load', '-l', 'command_type', flag_value='load', default=True, help='Run the command behind a shortcut')
@click.option('--save', '-s', 'command_type', flag_value='save', help='Save a new shortcut. How to give the arguments:\n0. the shortcut\n1. the type of backup to make\n2. the path of the folder to backup\n3. the path of the goal directory\n4. the name of the backup')
@click.option('--list', '-lt', 'command_type', flag_value='list', help='List all the shortcuts')
@click.argument('shortcut_command', nargs=1)
@click.pass_context
def sc(ctx, command_type, shortcut_command):
    '''Save or load a shortcut'''
    if command_type == 'load':
        # get the data behind the shortcut
        backup_type, folder, directory, name = short.evaluateShortcut(
            shortcut_command[0])
        click.echo(
            f'Running shortcut... \nCommand: backup make --{backup_type} --folder {folder} --directory {directory} --name {name}')

        # run the command
        ctx.invoke(make, backup_type=backup_type, folder=folder,
                   directory=directory, name=name)
    elif command_type == 'save':
        # check if there are all agruments
        if len(shortcut_command) < 5:
            click.echo(f'Error: Missing argument "SHORTCUT_COMMAND...".')
        elif len(shortcut_command) > 5:
            click.echo(f'Error: Got unexpected extra arguments')
        
        # define the arguments
        shortcut = shortcut_command[0]
        backup_type = shortcut_command[1]
        folder = shortcut_command[2]
        directory = shortcut_command[3]
        name = shortcut_command[4]

        # do the work
        click.echo(
            f'Adding shortcut {shortcut}...\nCommand: backup make --{backup_type} -f {folder} -d {directory} -n {name}')
        if short.addShortcut(shortcut, backup_type, folder, directory, name):
            click.echo(f'Successfully saved {shortcut}')
        else:
            click.echo(f'Error: the shortcut {shortcut} cannot exist twice')
    elif command_type == 'list':
        shortcut_list = short.listShortcuts()
        click.echo(f'{shortcut_list}')

#
# OTHER FUNCTIONS
#

def makeName(name, folder_dir, directory):
    # check if it is only a default value
    print(name, folder_dir, directory)
    if name == 'default':
        # get the name of the directory
        name = folder_dir[folder_dir.rindex("\\"):] + '__backup'
        print(name)

    # get the directory
    return directory + '\\' + name


def resolveDirectory(directory):
    # check if there are any shortcuts (announced by a #)
    if '#' in directory:
        hashtag = directory.index('#')

        # check if the shortcut is at the beginning of the path
        if hashtag > 3:
            click.echo(f'Error: path shortcuts need to be at the beginning of a path')
            exit(1)
        # check if there is only one shortcut
        elif '#' in directory[hashtag + 2:]:
            click.echo(f'Error: only 1 shortcut is allowed')
            exit(1)
        # if everything is ok
        else:
            shortcut = directory[hashtag:hashtag + 2]

            if shortcut == '#d':
                directory = directory[hashtag + 2:]
                directory = 'C:\\Users\\Nutzer\\Desktop' + directory
            elif shortcut == '#s':
                directory = directory[hashtag + 2:]
                directory = 'C:\\Users\\Nutzer\\Desktop\\School' + directory
            elif shortcut == '#p':
                directory = directory[hashtag + 2:]
                directory = 'C:\\Users\\Nutzer\\Desktop\\Private' + directory

    return directory


if __name__ == "__main__":
    main()
