# -*- mode: python -*-

block_cipher = None
added_files = [
    ('profiles/default-profile.ini', 'default-profile.ini'),
    ('bin', 'bin'),
]

a = Analysis(['multipartprintpy\\gui.py'],
             pathex=['C:\\Users\\m78162\\Documents\\code\\muli-part-print-cost'],
             binaries=[],
             datas=added_files,
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
          [],
          exclude_binaries=True,
          name='multi-part-print-cost-debug',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='multi-part-print-cost-debug')
