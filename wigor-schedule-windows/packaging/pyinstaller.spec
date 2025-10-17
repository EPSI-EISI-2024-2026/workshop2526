# This file is used by PyInstaller to create the executable for the Windows application.
# It specifies the files to include and any additional options for packaging.

block_cipher = None

a = Analysis(['../src/main.py'],
             pathex=['../src'],
             binaries=[],
             datas=[('../src/*.py', 'src'), ('../requirements.txt', '.'), ('../README.md', '.')], 
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
           cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='wigor_schedule',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='wigor_schedule')