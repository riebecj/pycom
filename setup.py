from setuptools import setup
setup(
    name='pycom.py',
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'pycom=pycom:main'
        ]
    }
)