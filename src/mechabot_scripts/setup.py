from setuptools import find_packages, setup

package_name = 'mechabot_scripts'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='utk',
    maintainer_email='kutkarsh706@gmail.com',
    description='Helper scripts for MechaBot simulation.',
    license='NOASSERTION',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'read_lidar = mechabot_scripts.read_lidar:main',
            'read_imu = mechabot_scripts.read_imu:main',
            'read_camera = mechabot_scripts.read_camera:main',
            'obstacle_avoidance = mechabot_scripts.obstacle_avoidance:main',
            'send_nav_goal = mechabot_scripts.send_nav_goal:main',
        ],
    },
)
