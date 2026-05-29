# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hidden_libs = [
    "pymysql",
    "requests",
    "sqlalchemy",
    "Image_GUI.main_page",
    "Excel_Main_GUI.MergeExcel",
    "Modern_GUI.main",
    "numpy",
    "pandas",
    "numpy._core._exceptions",
    "numpy._core._methods",
    "numpy._core._multiarray_umath"
]

a = Analysis(
    ['login_system.py'],
    pathex=[
        '.',
        'Excel_Main_GUI',
        'Excel_Main_GUI/PyMergeExcel',
        'Image_GUI',
        'Modern_GUI'
    ],
    binaries=[],
    datas=[
        ('app/images', 'app/images'),
        ('Excel_Main_GUI/PyMergeExcel/text.txt', '.'),
        ('Excel_Main_GUI/ico', 'Excel_Main_GUI/ico'),
        ('Modern_GUI/icon.ico', 'Modern_GUI'),
        ('Modern_GUI/images', 'Modern_GUI/images'),
        ('Modern_GUI/themes', 'Modern_GUI/themes')
    ],
    hiddenimports=hidden_libs,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LoginSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app\\images\\ico\\cactus.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LoginSystem',
)