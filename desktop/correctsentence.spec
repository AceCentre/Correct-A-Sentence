# -*- mode: python ; coding: utf-8 -*-

datas = [(r'C:\Users\willwade\AppData\Roaming\Python\Python38\site-packages\onnxruntime\capi\*.dll', 'onnxruntime\capi')]
datas += [(r'C:\Users\willwade\AppData\Roaming\Python\Python38\site-packages\onnxruntime\capi\*.pyd', 'onnxruntime\capi')]
datas += [('models','models')]

a = Analysis(
    ['correctsentence.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='correctsentence',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='correctsentence',
)
