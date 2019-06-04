# -*- mode: python -*-

block_cipher = None


a = Analysis(['multipartprintpy\\gui.py'],
             pathex=['C:\\Users\\brian\\Documents\\code\\muli-part-print-cost'],
             binaries=[],
             datas=[
               ('profiles/default-profile.ini', 'default-profile.ini'),
               ('bin/Slic3rPE-1.42.0-beta2+win64-full-201904140830', 'bin')
             ],
             hiddenimports=[],
             hookspath=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='multi-part-print-cost',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
