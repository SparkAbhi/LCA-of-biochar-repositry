# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\spark\\OneDrive\\Abhijeet Project\\src'],
             binaries=[],
             datas=[('../src/impactAssesment/impactAssesment.ui', 'impactAssesment'), ('../src/massBalance/massBalance.ui', 'massBalance'), ('../src/massBalance/massBalanceDataEntryDialog.ui', 'massBalance'), ('../src/energyAnalysis/energyAnalysis.ui', 'energyAnalysis'), ('../src/energyAnalysis/energyAnalysisDataEntryDialog.ui', 'energyAnalysis'), ('../src/exergyAnalysis/exergyAnalysis.ui', 'exergyAnalysis'), ('../src/exergyAnalysis/exergyAnalysisDataEntryDialog.ui', 'exergyAnalysis'), ('../src/start/start.ui', 'start'), ('../src/start/mainDatabase.db', 'start')],
             hiddenimports=['babel.numbers', 'PySide2.QtXml', 'PySide2.QtUiTools'],
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
          name='main',
          debug=False,
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
               upx_exclude=[],
               name='main')
