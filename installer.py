import os
import PyInstaller.__main__

# PyInstaller.__main__.run([
#     '--name=security_auth_check',
#     '--noconfirm',
#     'create_token.py'
# ])

PyInstaller.__main__.run([
    '--name=security_auth',
    '--noconfirm',
    '--onefile',
    '--add-data=init/DB.ensql;.',
    # '--add-data=init/DB.sql;.',
    # '--add-data=dist/security_auth_check/security_auth_check.exe;.',
    'run.py'
])
