from distutils.core import setup

setup(
    name='My Diary',
    version='0.1',
    author='Ondřej Divina & Jan Melichařík',
    author_email='Ondra.Divina@seznam.cz',
    scripts=['diary_app.py', 'bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='My Diary is the app for storing your diary records.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pyperclip",
    ]
)
