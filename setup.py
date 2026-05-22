from setuptools import setup

APP = ['frog_pet_qt.py']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PyQt5'],
    'includes': ['PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore'],
}

setup(
    app=APP,
    name='Frog Pet',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
