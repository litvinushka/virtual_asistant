from setuptools import setup, find_packages

setup(
    name='virtual_assistant_py_wizards',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'virtual_assistant=virtual_assistant.main:main',
        ],
    },
)
