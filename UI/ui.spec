# Note - references to files must be absolute!
# If you are running this script from any other machine than Tom's (Old Sebs) Laptop,
# ensure you update the file references accordingly
# -*- mode: python -*-

block_cipher = None


a = Analysis(['ui.py'],
             pathex=['C:\\Users\\Seb\\Documents\\GitHub\\DataLogger\\UI'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ui',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True,
          icon='C:\\Users\\Seb\\Documents\\GitHub\\DataLogger\\UI\\icon.ico')

# Create folder structure and move Config and Readme
import shutil
import os
shutil.copyfile('progConf.ini', '{0}/progConf.ini'.format(DISTPATH))
shutil.copyfile('READMEDIST.txt', '{0}/README.txt'.format(DISTPATH))
dirList = ["files", "files/inbox", "files/converted", "files/outbox"]
for directory in dirList:
    os.makedirs("{}/{}".format(DISTPATH, directory))
