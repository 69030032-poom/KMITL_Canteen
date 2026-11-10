import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

import customtkinter as ctk
from Frontend.app import CanteenApp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--role', choices=['customer', 'shop'])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    folder = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    if args.role is None:
        for role in ['customer', 'shop']:
            command = [sys.executable] if getattr(sys, 'frozen', False) else [sys.executable, str(Path(__file__).resolve())]
            subprocess.Popen(command + ['--role', role], cwd=folder)
        return
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    app = CanteenApp(role=args.role)
    if args.check:
        from Backend import database, users
        username = 'demo_customer' if args.role == 'customer' else 'demo_shop'
        app.login_finished(users.login(username, 'Demo12345'))
        if args.role == 'customer':
            app.show_menu('คณะครุศาสตร์', 'ร้านครัวสิริ')
        app.update()
        if args.role == 'shop':
            from Frontend.shop_menu_page import ShopMenuPage
            editor = ShopMenuPage(app)
            editor.update()
            editor.destroy()
        connection = database.connect_database()
        assert connection.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        assert not connection.execute('PRAGMA foreign_key_check').fetchall()
        connection.close()
        report = {'role': args.role, 'title': app.title(), 'database': str(database.database_file), 'login_and_page': 'PASS'}
        (folder / ('check_' + args.role + '.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        app.destroy()
    else:
        app.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        folder = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
        (folder / 'startup_error.log').write_text(traceback.format_exc(), encoding='utf-8')
        raise
