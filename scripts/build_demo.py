"""Build an isolated Windows demo from tracked source and SQL fixtures."""
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from Backend import database, users

output = ROOT / 'outputs' / 'demo_003_build'
stage = output / 'source'
stage.mkdir(parents=True, exist_ok=True)
for name in ('Backend', 'Frontend', 'assets'):
    shutil.copytree(ROOT / name, stage / name, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', 'payment_qr.png'))
shutil.copy2(ROOT / 'scripts' / 'demo_main.py', stage / 'main.py')
command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--windowed', '--onedir',
           '--name', 'Demo_003', '--collect-all', 'customtkinter', '--add-data', 'assets;assets',
           '--icon', 'assets/app_icon/canteen_icon_v2.ico', '--distpath', str(output/'dist'),
           '--workpath', str(output/'work'), 'main.py']
subprocess.run(command, cwd=stage, check=True)
release = output / 'dist' / 'Demo_003'
folder = release / 'Database SQLite'
folder.mkdir(exist_ok=True)
database.database_file = folder / 'canteen.db'
if database.database_file.exists():
    raise RuntimeError('Use a fresh output folder; demo database already exists')
connection = sqlite3.connect(database.database_file)
for name in ('schema.sql','sample_data.sql','01_add_users.sql','03_education_real_shops.sql',
             '04_drink_variants.sql','05_phee_chai_menus.sql','06_noodle_options.sql'):
    connection.executescript((ROOT/'Database SQLite'/name).read_text(encoding='utf-8'))
connection.close()
database.upgrade_database()
users.register_customer('demo_customer','Demo12345','Demo Customer')
connection = database.connect_database()
shop_id = connection.execute("SELECT shop_id FROM shops WHERE name='ร้านครัวสิริ'").fetchone()[0]
connection.close()
user_id = users.register_shop('demo_shop','Demo12345','Demo Shop',shop_id)
connection = database.connect_database()
with connection:
    connection.execute('UPDATE users SET is_approved=1 WHERE user_id=?',(user_id,))
connection.close()
shutil.copy2(ROOT/'scripts'/'DEMO_READ_ME.txt', release/'READ_ME.txt')
print(release)
