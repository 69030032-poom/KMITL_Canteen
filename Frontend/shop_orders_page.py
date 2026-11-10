import json
import sqlite3
from functools import partial
from tkinter import messagebox
import customtkinter as ctk
from Backend import users, shop_orders
from Frontend.auto_refresh_frame import AutoRefreshFrame
from Frontend.menu_images import get_menu_image
from Frontend.theme import ORANGE, ORANGE_HOVER, TEXT, MUTED, CREAM, PEACH, BORDER


class ShopOrdersPage(AutoRefreshFrame):
    def __init__(self,parent,go_back):
        super().__init__(parent,fg_color=CREAM)
        self.go_back=go_back
        self.selected_order=None
        self.filter_name='ทั้งหมด'
        self.grid_columnconfigure(0,weight=2,uniform='orders')
        self.grid_columnconfigure(1,weight=3,uniform='orders')
        self.grid_rowconfigure(2,weight=1)
        self.heading=ctk.CTkLabel(self,text='',font=ctk.CTkFont(size=23,weight='bold'),text_color=TEXT)
        self.heading.grid(row=0,column=0,columnspan=2,sticky='w',padx=12,pady=(4,12))
        self.filters=ctk.CTkSegmentedButton(self,values=['ทั้งหมด','รอตรวจชำระ','กำลังเตรียม','พร้อมรับ','รับแล้ว'],
            command=self.change_filter,selected_color=PEACH,selected_hover_color='#F5D5BF',unselected_color='white',unselected_hover_color=CREAM,text_color=TEXT,fg_color=BORDER,font=ctk.CTkFont(size=13))
        self.filters.set('ทั้งหมด')
        self.filters.grid(row=1,column=0,columnspan=2,sticky='ew',padx=12,pady=(0,12))
        self.order_list=ctk.CTkScrollableFrame(self,fg_color='transparent')
        self.order_list.grid(row=2,column=0,sticky='nsew',padx=(4,12))
        self.detail_panel=ctk.CTkFrame(self,fg_color='white',corner_radius=14,border_width=1,border_color=BORDER)
        self.detail_panel.grid(row=2,column=1,sticky='nsew',padx=(0,12))
        self.detail_panel.grid_columnconfigure(0,weight=1)
        self.detail_panel.grid_rowconfigure(0,weight=1)
        self.detail_body=ctk.CTkScrollableFrame(self.detail_panel,fg_color='transparent')
        self.detail_body.grid(row=0,column=0,sticky='nsew',padx=12,pady=12)
        self.actions=ctk.CTkFrame(self.detail_panel,fg_color='white')
        self.actions.grid(row=1,column=0,sticky='ew',padx=16,pady=12)
        self.feedback=ctk.CTkLabel(self,text='อัปเดตอัตโนมัติทุก 3 วินาที',text_color=MUTED)
        self.feedback.grid(row=3,column=0,columnspan=2,sticky='w',padx=12,pady=8)
        self.refresh_page=self.show_orders
        self.show_orders()

    def change_filter(self,value):
        self.filter_name=value
        self.show_orders()

    def show_orders(self):
        try:
            shop=users.get_my_shop()
            self.canteen,self.shop=shop['canteen_name'],shop['shop_name']
            rows=shop_orders.read_orders(self.canteen,self.shop)
        except (sqlite3.Error,ValueError):
            self.feedback.configure(text='อ่านออเดอร์ไม่สำเร็จ กำลังลองใหม่',text_color=ORANGE)
            return False
        self.heading.configure(text=self.shop)
        self.feedback.configure(text='อัปเดตอัตโนมัติทุก 3 วินาที',text_color=MUTED)
        statuses={'รอตรวจชำระ':('awaiting_payment_review','payment_rejected'),
                  'กำลังเตรียม':('paid','preparing'),'พร้อมรับ':('ready',),'รับแล้ว':('completed',)}
        visible=[r for r in rows if self.filter_name=='ทั้งหมด' or r['status'] in statuses[self.filter_name]]
        for w in self.order_list.winfo_children():
            w.destroy()
        for order in visible:
            selected=order['order_id']==self.selected_order
            box=ctk.CTkFrame(self.order_list,fg_color=PEACH if selected else 'white',corner_radius=12,border_width=1,border_color=ORANGE if selected else BORDER)
            box.pack(fill='x',pady=5,padx=2)
            text=f"#{order['order_id']:04d}   {order['customer_name']}\nรับ {order['pickup_date']}  {order['pickup_time']}\n{order['total']} บาท · {shop_orders.status_names.get(order['status'],order['status'])}"
            ctk.CTkButton(box,text=text,anchor='w',height=100,fg_color='transparent',hover_color=PEACH,text_color=TEXT,
                font=ctk.CTkFont(size=14),command=partial(self.show_details,order['order_id'])).pack(fill='x',padx=10,pady=8)
        if not visible:
            ctk.CTkLabel(self.order_list,text='ยังไม่มีออเดอร์ในกลุ่มนี้',text_color=MUTED).pack(pady=30)
        order=next((r for r in rows if r['order_id']==self.selected_order),None)
        return self.draw_details(order)

    def show_details(self,order_id):
        self.selected_order=order_id
        return self.show_orders()

    def label(self,text,bold=False):
        ctk.CTkLabel(self.detail_body,text=text,anchor='w',justify='left',wraplength=370,
            text_color=TEXT,font=ctk.CTkFont(size=16 if bold else 14,weight='bold' if bold else 'normal')).pack(fill='x',pady=7,padx=8)

    def draw_details(self,order):
        for parent in (self.detail_body,self.actions):
            for w in parent.winfo_children():
                w.destroy()
        if order is None:
            self.label('เลือกออเดอร์ทางซ้ายเพื่อดูรายละเอียด',True)
            return
        oid=order['order_id']
        self.label(f'ออเดอร์ #{oid:04d}',True)
        self.label(f"ผู้รับ: {order['customer_name']}\nโทร: {order['phone']}\nรับ {order['pickup_date']} เวลา {order['pickup_time']}")
        status=order['status']
        self.label('สถานะ: '+shop_orders.status_names.get(status,status),True)
        ctk.CTkFrame(self.detail_body,height=1,fg_color=BORDER).pack(fill='x',pady=10)
        try:
            items=shop_orders.read_items(oid,self.canteen,self.shop)
        except (sqlite3.Error,ValueError):
            self.label('อ่านรายการอาหารไม่สำเร็จ กรุณาเลือกออเดอร์อีกครั้ง')
            return False
        for item in items:
            item_row=ctk.CTkFrame(self.detail_body,fg_color='transparent')
            item_row.pack(fill='x',padx=8,pady=(8,2))
            picture=get_menu_image(item['menu_name'],(90,75))
            if picture:
                photo=ctk.CTkLabel(item_row,text='',image=picture)
                photo.image=picture
                photo.pack(side='left',padx=(0,12))
            ctk.CTkLabel(item_row,text=f"{item['menu_name']} × {item['quantity']}\n{item['unit_price']*item['quantity']} บาท",
                text_color=TEXT,font=ctk.CTkFont(size=16,weight="bold"),justify="left",wraplength=260).pack(side="left")
            try:
                choices=json.loads(item['options'])
                if choices:self.label(' · '.join(choices))
            except (ValueError,TypeError):
                self.label(str(item['options']))
            if item['note']:self.label('หมายเหตุ: '+item['note'])
        self.label(f"ยอดรวม {order['total']} บาท",True)
        if status=='awaiting_payment_review':
            self.label('สำหรับสาธิต: ตรวจยอดเงินด้วยตัวเองก่อนยืนยัน ระบบไม่ตรวจธนาคารอัตโนมัติ')
        actions={'paid':'ตรวจเงินเข้าแล้ว — ยืนยัน','payment_rejected':'ยังยืนยันการชำระไม่ได้',
            'awaiting_payment_review':'ตรวจชำระอีกครั้ง','preparing':'รับออเดอร์และเริ่มเตรียม',
            'ready':'อาหารพร้อมรับ','completed':'ส่งอาหารให้ผู้รับแล้ว'}
        for target in shop_orders.next_statuses.get(status,()):
            secondary=target=='payment_rejected'
            ctk.CTkButton(self.actions,text=actions[target],height=42,fg_color=PEACH if secondary else ORANGE,
                hover_color='#F5D5BF' if secondary else ORANGE_HOVER,text_color=TEXT if secondary else 'white',
                font=ctk.CTkFont(size=15,weight='bold'),command=partial(self.update_status,oid,status,target)).pack(fill='x',pady=4)

    def update_status(self, order_id, old_status, new_status):
        self.refresh_paused = True
        try:
            self.confirm_status_change(order_id, old_status, new_status)
        finally:
            self.refresh_paused = False

    def confirm_status_change(self, order_id, old_status, new_status):
        if new_status == 'paid':
            confirmed = messagebox.askyesno(
                'ยืนยันการตรวจรับเงิน',
                'คุณตรวจชื่อผู้โอนและยอดเงินเข้าครบแล้วใช่ไหม?\nระบบนี้ไม่ตรวจธนาคารอัตโนมัติ',
                parent=self,
            )
            if not confirmed:
                return
        try:
            shop_orders.change_status(order_id, self.canteen, self.shop, old_status, new_status)
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror('เปลี่ยนสถานะไม่สำเร็จ', str(error), parent=self)
        self.show_details(order_id)
