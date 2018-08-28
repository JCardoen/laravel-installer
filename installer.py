import os

class Installer:
    projectName = ''
    databaseName = ''
    useLaradock = False

    def __init__(self):
        self.projectName = raw_input('Name of project: ')
        self.projectLocation = raw_input('Location of project folder: ')
        self.databaseName = raw_input('Name of database: ')
        print('Composer installer')
        os.system('composer global require "laravel/installer"')
        self.laravel_new()
        self.init_laradock()
        self.start_laradock()

    def start_laradock(self):
        print('Starting laradock...')
        try:
            os.system('cd {}/laradock/ && docker-compose -d up nginx workspace mysql'.format(self.projectLocation))
            print('Laradock started')
        except Exception as ex:
            print('ERROR while trying to start Laradock: {}'.format(ex.message))

    def laravel_new(self):
        os.system('composer create-project --prefer-dist laravel/laravel {}/{}'.format(self.projectLocation, self.projectName))
        self.setup_laravel_env()

    def init_laradock(self):
        print('Checking if laradock exists...')
        laradockInstallation = os.path.exists('{}/laradock'.format(self.projectLocation))
        if not laradockInstallation:
            print('Cloning laradock repository...')
            os.system('git clone https://github.com/Laradock/laradock.git {}/laradock'.format(self.projectLocation))
            print('Done copying repository')
            print('Adjusting necessary files...')

        self.setup_laradock_env()

    def setup_laradock_env(self):
        with open('{}/laradock/env-example'.format(self.projectLocation)) as f:
            envFile = f.read().replace('APP_CODE_PATH_HOST=../', 'APP_CODE_PATH_HOST=../{}/'.format(self.projectName))
            envFile = envFile.replace('APPLICATION=../project-z/', 'APPLICATION=../{}/'.format(self.projectName))
            envFile = envFile.replace('MYSQL_DATABASE = default/', 'MYSQL_DATABASE = {}'.format(self.databaseName))

        with open('{}/laradock/.env'.format(self.projectLocation), 'w+') as f:
            f.write(envFile)

    def setup_laravel_env(self):
        with open('{}/{}/.env'.format(self.projectLocation, self.projectName) ) as f:
            print('Setting MySQL Host')
            envFile = f.read().replace('DB_HOST=127.0.0.1', 'DB_HOST=mysql')
            print('Setting MySQL DATABASE')
            envFile = envFile.replace('DB_DATABASE=homestead', 'DB_DATABASE={}'.format(self.databaseName))
            print('Setting MySQL USERNAME')
            envFile = envFile.replace('DB_USERNAME=homestead', 'DB_USERNAME=root'.format(self.databaseName))
            print('Setting MySQL PASSWORD')
            envFile = envFile.replace('DB_PASSWORD=secret', 'DB_PASSWORD=root')

        with open('{}/{}/.env'.format(self.projectLocation, self.projectName), 'w' ) as f:
            f.write(envFile)
