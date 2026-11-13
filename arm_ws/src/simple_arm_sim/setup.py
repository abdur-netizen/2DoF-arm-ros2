import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'simple_arm_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdur',
    maintainer_email='abdur@todo.todo',
    description='Simple 2-DOF robotic arm simulation',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fk_node = simple_arm_sim.fk_node:main',
            'ik_node = simple_arm_sim.ik_node:main'
        ],
    },
)
