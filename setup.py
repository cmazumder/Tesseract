from setuptools import setup

setup(
    name='DeployBuilds_from_TeamCity',
    version='2.3',
    install_requires=['psutil==5.6.6',
                      'tqdm==4.46.1',
                      'pyodbc==4.0.27',
                      'colorama==0.4.1',
                      'requests==2.22.0',
                      'progressbar2==3.51.4'],
    url='',
    license='',
    author='Chayan Mazumder',
    author_email='',
    description='Download and setup builds from TeamCity'
)
