# -*- mode: python -*-

block_cipher = None


a = Analysis(['ControlDemonstrator.py'],
             pathex=['D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\ControlDemonstrator'],
             binaries=[],
             datas=[('applicationSettings.json', '.'),
                    ('README.md', '.'),
                    ('documentation/*', 'documentation'),
                    ('core/includeFileTemplates/c_template.h', 'core/includeFileTemplates'),
                    ('core/includeFileTemplates/c_template.c', 'core/includeFileTemplates'),
                    ('gui/resources/greenPlus.png', 'gui/resources'),
                    ('gui/resources/ic.png', 'gui/resources'),
                    ('gui/resources/pause.png', 'gui/resources'),
                    ('gui/resources/play.png', 'gui/resources'),
                    ('gui/resources/redCross.png', 'gui/resources'),
                    ('gui/resources/settings.png', 'gui/resources')
                    ],
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
          exclude_binaries=True,
          name='ControlDemonstrator',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='D:\\00 eigene Daten\\000 FH\\S 4\\Regelungstechnik\\Regelungsversuch\\ControlDemonstrator\\ic.ico'
          )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ControlDemonstrator')
