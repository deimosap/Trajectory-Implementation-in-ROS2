from setuptools import find_packages, setup
## glob imported for launch script
from glob import glob

package_name = 'ex1'

## add launch to data_files
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='deimos',
    maintainer_email='deimos@todo.todo',
    description='TODO: Package description',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'question_1 = ex1.question_1:main',
            'question_2 = ex1.question_2:main',
            'question_3 = ex1.question_3:main'
        ],
    },
)
