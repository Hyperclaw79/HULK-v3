# -*- mode: python ; coding: utf-8 -*-
import PyInstaller.config
import platform
PyInstaller.config.CONF['distpath'] = f"./dist/{platform.system().lower()}"

block_cipher = None


client = Analysis(
    ['client/hulk.py'],
    pathex=['client'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

client_pyz = PYZ(client.pure, client.zipped_data, cipher=block_cipher)

client_exe = EXE(
    client_pyz,
    client.scripts,
    client.binaries,
    client.zipfiles,
    client.datas,
    [],
    name='hulk_client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


server = Analysis(
    ['server/hulk_server.py'],
    pathex=['server'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

server_pyz = PYZ(server.pure, server.zipped_data, cipher=block_cipher)

server_exe = EXE(
    server_pyz,
    server.scripts,
    server.binaries,
    server.zipfiles,
    server.datas,
    [],
    name='hulk_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


launcher = Analysis(
    ['hulk_launcher.py'],
    pathex=['server,client'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

launcher_pyz = PYZ(launcher.pure, launcher.zipped_data, cipher=block_cipher)

launcher_exe = EXE(
    launcher_pyz,
    launcher.scripts,
    launcher.binaries,
    launcher.zipfiles,
    launcher.datas,
    [],
    name='hulk_launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)