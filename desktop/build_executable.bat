python -m PyInstaller correctsentence.spec --noconfirm --upx-dir=C:\upx
python -m PyInstaller client.spec --noconfirm --upx-dir=C:\upx
python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean --upx-dir=C:\upx
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss