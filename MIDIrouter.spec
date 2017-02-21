# -*- mode: python -*-

block_cipher = None


a = Analysis(['midirouter.py'],
             pathex=['/Users/icaroferre/Documents/PycharmProjects/midiRouter'],
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
          name='MIDIrouter',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.icns')
app = BUNDLE(exe,
             name='MIDIrouter.app',
             icon='icon.icns',
             bundle_identifier=None,
             info_plist={
              'NSHighResolutionCapable': 'True',
              'CFBundleVersion': '1.0',
              'CFBundleShortVersionString' : '1.0',
              'SUPublicDSAKeyFile': 'dsa_pub.pem',
              'SUFeedURL' : "https://s3.amazonaws.com/files.icaroferre.com/midirouter/appcast.xml"
              },)
