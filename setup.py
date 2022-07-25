from setuptools import setup
setup(
    name='pycom.py',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'pycom=pycom:main'
        ]
    }
)