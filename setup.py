import json
import os
import shutil

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'saika', 'config', 'path.json'), 'r') as f:
    config = json.loads(f.read())

major = config.get('major')
ordinary = config.get('ordinary')
minor = config.get('minor')

r = setup(
    name='saika.path',
    version='%s.%s.%s' % (major, ordinary, minor),
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

if 'upload' in sorted(r.command_options.keys()):
    config['minor'] += 1
    with open(os.path.join(os.path.dirname(__file__), 'saika', 'config', 'path.json'), 'w') as f:
        f.write(json.dumps(config))

for dir in os.listdir('./'):
    fullpath = os.path.join(os.path.dirname(__file__), dir)
    if os.path.isdir(fullpath):
        if dir in ['dist', 'build'] or dir.endswith('.egg-info'):
            shutil.rmtree(fullpath)