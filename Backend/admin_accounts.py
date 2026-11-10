"""Run only by the trusted owner of the computer/database."""
import argparse
from Backend import database


def main():
    parser = argparse.ArgumentParser(description='จัดการบัญชีโดยผู้ดูแลเครื่องเท่านั้น')
    parser.add_argument('action',choices=['list','approve','suspend','restore'])
    parser.add_argument('--user-id',type=int)
    parser.add_argument('--shop-id',type=int)
    args=parser.parse_args()
    database.upgrade_database()
    connection=database.connect_database()
    try:
        if args.action=='list':
            for row in connection.execute('SELECT user_id,username,role,shop_id,is_approved,is_suspended FROM users'):
                print(row)
            return
        if args.user_id is None:
            parser.error('ต้องระบุ --user-id')
        with connection:
            if args.action=='approve':
                if args.shop_id is None: parser.error('ต้องระบุ --shop-id หลังตรวจสอบเจ้าของร้านแล้ว')
                cursor=connection.execute("UPDATE users SET shop_id=?,is_approved=1 WHERE user_id=? AND role='shop' AND EXISTS(SELECT 1 FROM shops WHERE shop_id=?)",(args.shop_id,args.user_id,args.shop_id))
            else:
                cursor=connection.execute('UPDATE users SET is_suspended=? WHERE user_id=?',(int(args.action=='suspend'),args.user_id))
            if cursor.rowcount!=1: raise ValueError('ไม่พบบัญชีหรือร้านที่ระบุ')
        print('บันทึกแล้ว')
    finally:
        connection.close()

if __name__=='__main__':
    main()
