from setuptools import find_packages, setup

setup(
    name='saika.path',
    version='0.0.9',
    license='PSF',
    author='Mohanson',
    author_email='mohanson@outlook.com',
    url='https://github.com/Mohanson/saika.path',
    description='use files and paths for human beings',

    namespace_packages=['saika'],
    entry_points={
        'console_scripts': [
            'saika.path.clean=scripts.clean:main'
        ]
    },
    packages=find_packages(),
    package_data={
        '': ['*.*']},
    install_requires=['saika.paramscheck'],
)