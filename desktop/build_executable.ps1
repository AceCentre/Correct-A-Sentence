cmd /c "python -m PyInstaller correctsentence_full.spec --noconfirm --upx-dir=C:\upx"
cmd /c "python -m PyInstaller client.spec --noconfirm --upx-dir=C:\upx"
cmd /c "python -m PyInstaller CreateGridset.py --noconsole --noconfirm --onedir --clean --upx-dir=C:\upx"
cmd /c '"C:\Program Files (x86)\NSIS\makensis.exe" .\buildscript.nsi'
