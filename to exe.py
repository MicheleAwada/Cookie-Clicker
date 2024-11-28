import PyInstaller.__main__
import os


baseDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(baseDir)
icon_path = os.path.join(baseDir, "extras/cookieclr.ico")  # "extras/icon.ico"
script_path = os.path.join(baseDir, "game.py")  # "game.py"
extras_path = os.path.join(baseDir, "extras")

PyInstaller.__main__.run([
    '--icon=' + icon_path,
    f'--add-data={extras_path}/*;extras',
    script_path
])