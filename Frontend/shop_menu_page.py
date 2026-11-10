import sqlite3
from tkinter import filedialog
import customtkinter as ctk
from Backend import shop_management, catalog, users
from Frontend.theme import ORANGE, ORANGE_HOVER, TEXT, CREAM


class ShopMenuPage(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('จัดการเมนูและเวลาร้าน')
        self.geometry('960x720')
        self.minsize(800,600)
        self.configure(fg_color=CREAM)
        self.menu_id = None
        self.image_file = None
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.list_frame = ctk.CTkScrollableFrame(self,width=240,fg_color='white')
        self.list_frame.grid(row=0,column=0,sticky='nsew',padx=12,pady=12)
        self.form = ctk.CTkScrollableFrame(self,fg_color='white')
        self.form.grid(row=0,column=1,sticky='nsew',padx=(0,12),pady=12)
        self.name = self.entry('ชื่อเมนู')
        self.price = self.entry('ราคาเริ่มต้น (บาท)')
        self.available = ctk.CTkCheckBox(self.form,text='เปิดขายเมนูนี้',text_color=TEXT,fg_color=ORANGE)
        self.available.pack(anchor='w',padx=16,pady=10)
        self.available.select()
        self.button(self.form,'เลือกรูปเมนู',self.choose_image)
        self.photo_label = ctk.CTkLabel(self.form,text='ยังไม่ได้เลือกรูป',text_color=TEXT)
        self.photo_label.pack()
        self.variant_rows = []
        self.option_rows = []
        ctk.CTkLabel(self.form,text='รูปแบบ / ขนาด — ราคาเต็ม เช่น เย็น 40 บาท',text_color=TEXT).pack(pady=(18,4))
        self.variants = ctk.CTkFrame(self.form,fg_color='transparent',height=1); self.variants.pack(fill='x')
        self.button(self.form,'เพิ่มรูปแบบหรือขนาด',lambda:self.add_row(False))
        ctk.CTkLabel(self.form,text='ตัวเลือกเสริม — กลุ่ม / ชื่อ / ราคาบวกเพิ่ม',text_color=TEXT).pack(pady=(18,4))
        self.options = ctk.CTkFrame(self.form,fg_color='transparent',height=1); self.options.pack(fill='x')
        self.button(self.form,'เพิ่มตัวเลือก เช่น เส้น / เส้นเล็ก / 0',lambda:self.add_row(True))
        self.footer = ctk.CTkFrame(self,fg_color='white')
        self.footer.grid(row=1,column=1,sticky='ew',padx=(0,12),pady=(0,12))
        self.button(self.footer,'บันทึกเมนู',self.save)
        self.message = ctk.CTkLabel(self.footer,text='',wraplength=450,text_color=ORANGE); self.message.pack(pady=8)
        ctk.CTkLabel(self.form,text='เวลารับอาหารและจำนวนคิว',font=ctk.CTkFont(size=18,weight='bold'),text_color=TEXT).pack(pady=(24,8))
        self.opening = self.entry('เปิดรับ HH:MM')
        self.closing = self.entry('ปิดรับ HH:MM')
        self.capacity = self.entry('จำนวนออเดอร์สูงสุดต่อ 15 นาที')
        self.active = ctk.CTkCheckBox(self.form,text='เปิดรับออเดอร์ใหม่',text_color=TEXT,fg_color=ORANGE); self.active.pack(pady=8)
        self.button(self.form,'บันทึกเวลาร้าน',self.save_hours)
        shop = users.get_my_shop()
        row = catalog.read_rows('SELECT * FROM shops WHERE shop_id=?',(shop['shop_id'],))[0]
        for entry,key in ((self.opening,'opening_time'),(self.closing,'closing_time'),(self.capacity,'slot_capacity')):
            entry.insert(0,str(row[key]))
        if row['is_active']: self.active.select()
        self.refresh_list()

    def entry(self,label):
        ctk.CTkLabel(self.form,text=label,text_color=TEXT,anchor='w').pack(fill='x',padx=16,pady=(10,3))
        entry=ctk.CTkEntry(self.form,height=36,fg_color='#FAF7F2',text_color=TEXT); entry.pack(fill='x',padx=16)
        return entry

    def button(self,parent,text,command):
        ctk.CTkButton(parent,text=text,command=command,fg_color=ORANGE,hover_color=ORANGE_HOVER,height=36).pack(fill='x',padx=16,pady=6)

    def refresh_list(self):
        for child in self.list_frame.winfo_children(): child.destroy()
        self.button(self.list_frame,'+ เพิ่มเมนูใหม่',lambda:self.load(None))
        for item in shop_management.read_menus():
            self.button(self.list_frame,item['name'],lambda item=item:self.load(item))

    def add_row(self,option,values=None):
        parent=self.options if option else self.variants
        rows=self.option_rows if option else self.variant_rows
        frame=ctk.CTkFrame(parent,fg_color='transparent'); frame.pack(fill='x',padx=16,pady=4)
        entries=[]
        for index in range(3 if option else 2):
            entry=ctk.CTkEntry(frame,width=120 if index==0 else 90,fg_color='#FAF7F2',text_color=TEXT)
            entry.pack(side='left',fill='x',expand=True,padx=2)
            if values: entry.insert(0,str(values[index]))
            entries.append(entry)
        rows.append(entries)
        def remove():
            rows.remove(entries); frame.destroy()
        ctk.CTkButton(frame,text='ลบ',width=44,command=remove,fg_color=ORANGE).pack(side='left',padx=4)

    def load(self,item):
        self.menu_id=item['menu_id'] if item else None
        self.image_file=None
        for entry,key in ((self.name,'name'),(self.price,'price')):
            entry.delete(0,'end'); entry.insert(0,str(item[key]) if item else '')
        self.available.select() if not item or item['is_available'] else self.available.deselect()
        self.photo_label.configure(text='ใช้รูปเดิม' if item else 'ยังไม่ได้เลือกรูป')
        for frame in (self.variants,self.options):
            for child in frame.winfo_children(): child.destroy()
        self.variant_rows=[]; self.option_rows=[]
        if item:
            variants,options=shop_management.read_choices(self.menu_id)
            for row in variants: self.add_row(False,row)
            for row in options: self.add_row(True,row)
        self.message.configure(text='')

    def choose_image(self):
        path=filedialog.askopenfilename(parent=self,filetypes=[('รูปภาพ','*.png *.jpg *.jpeg *.webp')])
        if path:
            self.image_file=path
            self.photo_label.configure(text=path.rsplit('/',1)[-1])

    def save(self):
        try:
            variants=[(row[0].get().strip(),int(row[1].get())) for row in self.variant_rows]
            options=[(row[0].get().strip(),row[1].get().strip(),int(row[2].get())) for row in self.option_rows]
            self.menu_id=shop_management.save_menu(self.menu_id,self.name.get(),int(self.price.get()),self.available.get(),variants,options,self.image_file)
            self.image_file=None
            self.refresh_list()
            self.message.configure(text='บันทึกแล้ว ลูกค้าจะเห็นข้อมูลใหม่เมื่อเปิดเมนูอีกครั้ง')
        except (ValueError,OSError,sqlite3.Error) as error:
            self.message.configure(text='บันทึกไม่สำเร็จ: '+str(error))

    def save_hours(self):
        try:
            shop_management.save_hours(self.opening.get(),self.closing.get(),int(self.capacity.get()),self.active.get())
            self.message.configure(text='บันทึกเวลาร้านแล้ว')
        except (ValueError,sqlite3.Error) as error:
            self.message.configure(text=str(error))
