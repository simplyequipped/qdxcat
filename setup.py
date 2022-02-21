import subprocess
from setuptools import setup

setup(
    name='qdx',
    version='0.1',
    description='QRP Labs QDX tranceiver control library',
    author='Simply Equipped LLC',
    author_email='info@simplyequipped.com',
    packages=['qdx'],
    install_requires=['pyserial', 'flask', 'waitress']
)

user = subprocess.check_output(['whoami']).decode('utf-8').strip()
groups = subprocess.check_output(['groups']).decode('utf-8').strip().split()[1:]

if 'dialout' not in groups:
    print('User \'' + user + '\' is not a member of the \'dialout\' group, which allows serial port access.')
    dialout_setup = input('Would you like to add \'' + user + '\' to the \'dialout\' group now? (yes/no): ')

    if dialout_setup.lower() in ['yes', 'y', '']:
        print('\nYou will be prompted for your sudo password now.')
        subprocess.call(['sudo', 'usermod', '-a', '-G', 'dialout', user])

        print('User \'' + user + '\' has been added to the \'dialout\' group.')
        print('Logout/login or restart for the group changes to take effect.')

    else:
        print('\nYou will need to either use \'sudo\' when running a program using this package,')
        print('or you can manually add a user to the \'dialout\' group using the following:')
        print('\tsudo usermod -a -G dialout user\n')
        print('Logout/login or restart will be required for the group changes to take effect.')

