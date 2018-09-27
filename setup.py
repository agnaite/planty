from setuptools import setup

setup(
    name='planty',
    packages=['views', 'reminder_sender'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
