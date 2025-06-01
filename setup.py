from setuptools import setup

APP = ['installer_macos.py']
DATA_FILES = [
    ('img', ['img/hello.png', 'img/mac.png']),  # include all images used
    ('', ['LICENSE'])  # other necessary files
]
OPTIONS = {
    'packages': ['customtkinter', 'PIL', 'wget', 'requests', 'CTkMessagebox', 'psutil', 'minecraft_launcher_lib'],
    "excludes": ["PyInstaller"],
    'iconfile': 'img/mac.icns',  # Optional: if you have a macOS icon file
    'plist': {
        'CFBundleName': 'Argon Installer',
        'CFBundleDisplayName': 'Argon Installer',
        'CFBundleIdentifier': 'com.vpun215.argoninstaller',
        'CFBundleVersion': '1.3.0',
        'CFBundleShortVersionString': '1.3',
        'NSPrincipalClass': 'NSApplication',
    },
    'resources': ['LICENSE'],
    "optimize": 2,
    "compressed": True
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)