from functools import partial
from pathlib import Path
import customtkinter as ctk
from PIL import Image
from Backend import menu, catalog
from Frontend.menu_images import get_menu_image
from Frontend.theme import add_canteen_art, ORANGE, ORANGE_HOVER, TEXT, MUTED, BORDER, CREAM, PEACH

WHITE = '#FFFFFF'


class MenuPage(ctk.CTkFrame):
    def __init__(self, parent, canteen_name, shop_name, add_to_cart, go_back, show_cart=None, cart_summary=None):
        super().__init__(parent, fg_color=CREAM)
        self.shop_name = shop_name
        self.canteen_name = canteen_name
        self.add_to_cart = add_to_cart
        self.go_back = go_back
        self.show_cart = show_cart
        self.cart_summary = cart_summary
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=340)
        self.grid_rowconfigure(1, weight=1)
        heading = ctk.CTkFrame(self, fg_color='transparent')
        heading.grid(row=0, column=0, sticky='ew', padx=12, pady=(8,12))
        art=add_canteen_art(heading,120,88)
        if art:art.pack(side='right',padx=8)
        ctk.CTkButton(heading,text='กลับไปร้านอาหาร',width=130,fg_color=PEACH,text_color=TEXT,
                      hover_color='#F5D5BF',command=go_back).pack(anchor='w',pady=(0,8))
        ctk.CTkLabel(heading,text=shop_name,font=ctk.CTkFont(size=25,weight='bold'),text_color=TEXT).pack(anchor='w')
        ctk.CTkLabel(heading,text=canteen_name,text_color=MUTED).pack(anchor='w')
        self.menu_list = ctk.CTkScrollableFrame(self,fg_color='transparent',corner_radius=0)
        self.menu_list.grid(row=1,column=0,sticky='nsew',padx=(6,12))
        self.menu_list.grid_columnconfigure(0,weight=1)
        self.menu_panel = ctk.CTkFrame(self,fg_color=WHITE,corner_radius=14,border_width=1,border_color=BORDER,width=340)
        self.menu_panel.grid(row=0,column=1,rowspan=3,sticky='nsew',padx=(0,8),pady=8)
        self.menu_panel.grid_propagate(False)
        self.menu_panel.grid_columnconfigure(0,weight=1)
        self.menu_panel.grid_rowconfigure(1,weight=1)
        self.cart_bar = ctk.CTkFrame(self,fg_color=PEACH,corner_radius=10)
        self.cart_bar.grid(row=2,column=0,sticky='ew',padx=12,pady=10)
        ctk.CTkLabel(heading,text='ภาพอาหารเป็นภาพประกอบเมนู',font=ctk.CTkFont(size=11),text_color=MUTED).pack(anchor='w')
        self.cart_label = ctk.CTkLabel(self.cart_bar,text='ตะกร้าร้านนี้',text_color=TEXT,font=ctk.CTkFont(size=14,weight='bold'))
        self.cart_label.pack(side='left',padx=12,pady=12)
        if show_cart:
            ctk.CTkButton(self.cart_bar,text='ดูตะกร้า',width=100,fg_color=ORANGE,hover_color=ORANGE_HOVER,command=show_cart).pack(side='right',padx=10)
        self.show_menu_list()
        self.clear_details()
        ctk.CTkLabel(self.details_area,text='เลือกเมนูทางซ้าย\nเพื่อปรับตัวเลือกอาหาร',font=ctk.CTkFont(size=17),text_color=MUTED).pack(pady=50)

    def update_cart_summary(self):
        if self.cart_summary:
            quantity,total=self.cart_summary()
            self.cart_label.configure(text=f'ตะกร้าร้านนี้ · {quantity} ชิ้น   {total} บาท')

    def show_menu_list(self):
        self.shop_id = catalog.get_shop(self.canteen_name,self.shop_name)['shop_id']
        self.menu_data = catalog.get_menu_data(self.canteen_name,self.shop_name)
        self.curry_shops,self.menus,self.shop_options,self.variants,self.item_options = self.menu_data
        for widget in self.menu_list.winfo_children():
            widget.destroy()
        self.menu_rows=[]
        self.menu_list.bind("<Configure>", self.arrange_menus, add="+")
        count=0
        if self.shop_name in self.curry_shops:
            curry=self.curry_shops[self.shop_name]
            if curry['dishes'] and curry['prices']:
                self.make_menu_row('ข้าวราดแกง',min(curry['prices'].values()))
                count+=1
        for name,price in self.menus[self.shop_name].items():
            self.make_menu_row(name,price)
            count+=1
        if not count:
            ctk.CTkLabel(self.menu_list,text='วันนี้ยังไม่มีเมนูพร้อมขาย',text_color=MUTED).pack(pady=30)
        self.update_cart_summary()

    def make_menu_row(self, name, price):
        row = ctk.CTkFrame(self.menu_list, fg_color=WHITE, corner_radius=12,
                          border_width=1, border_color=BORDER)
        self.menu_rows.append(row)
        row.grid(row=len(self.menu_rows)-1, column=0, sticky='ew', padx=4, pady=5)
        row.grid_columnconfigure(1, weight=1)
        picture = get_menu_image(name, (100, 100), self.shop_id)
        if picture:
            photo = ctk.CTkLabel(row, text='', image=picture, cursor='hand2')
            photo.image = picture
            photo.grid(row=0, column=0, rowspan=3, padx=(9, 8), pady=10)
            photo.bind('<Button-1>', lambda event: self.show_menu_details(name))
        ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=15, weight='bold'),
                    text_color=TEXT, anchor='w', justify='left', wraplength=175).grid(row=0,column=1,sticky='ew',padx=(0,10),pady=(12,2))
        ctk.CTkLabel(row,text=f'เริ่มต้น {price} บาท',text_color=MUTED,anchor='w').grid(row=1,column=1,sticky='ew',padx=(0,10))
        ctk.CTkButton(row,text='+ เลือก',width=80,height=30,fg_color=ORANGE,hover_color=ORANGE_HOVER,
                      command=partial(self.show_menu_details,name)).grid(row=2,column=1,sticky='e',padx=10,pady=(4,10))

    def arrange_menus(self,event):
        columns = 2 if event.width / self._get_widget_scaling() >= 620 else 1
        self.menu_list.grid_columnconfigure(0,weight=1,uniform='menus')
        self.menu_list.grid_columnconfigure(1,weight=1 if columns==2 else 0,uniform='menus' if columns==2 else '',minsize=0)
        for index,row in enumerate(self.menu_rows):
            row.grid(row=index//columns,column=index%columns,sticky='ew')

    def clear_details(self):
        for widget in self.menu_panel.winfo_children():
            widget.destroy()
        self.detail_title=ctk.CTkLabel(self.menu_panel,text='เลือกเมนู',font=ctk.CTkFont(size=20,weight='bold'),text_color=TEXT,wraplength=300)
        self.detail_title.grid(row=0,column=0,sticky='ew',padx=12,pady=14)
        self.details_area=ctk.CTkScrollableFrame(self.menu_panel,fg_color='transparent')
        self.details_area.grid(row=1,column=0,sticky='nsew',padx=8)
        self.action_area=ctk.CTkFrame(self.menu_panel,fg_color=WHITE)
        self.action_area.grid(row=2,column=0,sticky='ew',padx=14,pady=(4,14))
        self.message_label=ctk.CTkLabel(self.action_area,text='',wraplength=290,text_color=MUTED)


    def show_menu_details(self,menu_name):
        self.clear_details()
        self.detail_title.configure(text='เลือกเมนู')
        summary=ctk.CTkFrame(self.details_area,fg_color='transparent')
        summary.pack(fill='x',pady=(0,8))
        picture=get_menu_image(menu_name,(60,54), self.shop_id)
        if picture:
            photo=ctk.CTkLabel(summary,text='',image=picture)
            photo.image=picture
            photo.pack(side='left',padx=(0,10))
        ctk.CTkLabel(summary,text=menu_name,font=ctk.CTkFont(size=16,weight='bold'),
            text_color=TEXT,wraplength=205,justify='left').pack(side='left')
        if menu_name=='ข้าวราดแกง' and self.shop_name in self.curry_shops:
            self.show_curry_options(self.details_area)
        else:
            self.show_regular_menu(self.details_area,menu_name)

    def show_regular_menu(self, parent, menu_name):
        self.menu_choices = {}
        self.choice_buttons = {}
        self.menu_price_labels = {}
        price = menu.calculate_price(self.shop_name, menu_name, menu_data=self.menu_data)
        self.menu_choices[menu_name] = {}
        for group_name, choices in menu.get_option_groups(self.shop_name, menu_name, self.menu_data).items():
            if not choices:
                continue
            ctk.CTkLabel(
                parent, text=group_name, height=20, anchor="w", font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TEXT,
            ).pack(fill="x", pady=(6, 0))
            first_choice = list(choices)[0]
            choice_variable = ctk.StringVar(value=first_choice)
            self.menu_choices[menu_name][group_name] = choice_variable
            choices_frame = ctk.CTkFrame(parent, fg_color='transparent')
            choices_frame.pack(fill='x', pady=1)
            choices_frame.grid_columnconfigure((0, 1), weight=1)
            for index, (choice, extra_price) in enumerate(choices.items()):
                choice_text = choice + (f" (+{extra_price} บาท)" if extra_price > 0 else "")
                if group_name == 'รูปแบบ' and menu_name in self.variants:
                    choice_text = f"{choice} — {self.variants[menu_name][choice]} บาท"
                button=ctk.CTkButton(
                    choices_frame,text=choice_text,width=125,height=30,corner_radius=8,
                    font=ctk.CTkFont(size=12),fg_color=WHITE,text_color=TEXT,
                    border_width=1,border_color=BORDER,hover_color=PEACH,
                    command=partial(self.choose_option,menu_name,group_name,choice),
                )
                button.grid(row=index//2,column=index%2,sticky='ew',padx=3,pady=2)
                self.choice_buttons[(group_name,choice)]=button
        self.menu_price_labels[menu_name] = ctk.CTkLabel(
            self.action_area, text=f"ราคาต่อรายการ {price} บาท",
            font=ctk.CTkFont(size=14, weight="bold"), text_color=ORANGE,
        )
        self.menu_price_labels[menu_name].pack(pady=10)
        self.update_regular_price(menu_name)
        note_entry = ctk.CTkEntry(
            parent, placeholder_text="หมายเหตุถึงร้าน (ไม่บังคับ)", height=36,
        )
        note_entry.pack(fill="x", pady=5)
        ctk.CTkButton(
            self.action_area, text="เพิ่มลงตะกร้า", height=38, corner_radius=9,
            fg_color=ORANGE, hover_color=ORANGE_HOVER,
            command=partial(self.add_regular_item, menu_name, note_entry),
        ).pack(fill="x", pady=8)

    def choose_option(self, menu_name, group_name, choice):
        self.menu_choices[menu_name][group_name].set(choice)
        self.update_regular_price(menu_name)

    def get_selected_options(self, menu_name):
        return {
            group_name: choice_variable.get()
            for group_name, choice_variable in self.menu_choices[menu_name].items()
        }

    def update_regular_price(self, menu_name):
        selected_options = self.get_selected_options(menu_name)
        for (group,choice),button in self.choice_buttons.items():
            selected=selected_options[group]==choice
            button.configure(fg_color=PEACH if selected else WHITE,
                             border_color=ORANGE if selected else BORDER,
                             text_color=ORANGE if selected else TEXT)
        price = menu.calculate_price(
            self.shop_name, menu_name, selected_options=selected_options, menu_data=self.menu_data,
        )
        self.menu_price_labels[menu_name].configure(text=f"ราคาต่อรายการ {price} บาท")

    def add_regular_item(self, menu_name, note_entry):
        selected_options = self.get_selected_options(menu_name)
        price = menu.calculate_price(
            self.shop_name, menu_name, selected_options=selected_options, menu_data=self.menu_data,
        )
        options = [f"{group_name}: {choice}" for group_name, choice in selected_options.items()]
        self.add_to_cart(menu_name, price, options, note_entry.get())
        self.message_label.pack(pady=2)
        self.message_label.configure(text=f"เพิ่ม {menu_name} ลงตะกร้าแล้ว")
        self.update_cart_summary()

    def show_curry_options(self, parent):
        shop = self.curry_shops[self.shop_name]
        self.dish_count = ctk.IntVar(value=min(shop["prices"]))
        ctk.CTkLabel(parent, text="เลือกราคาและกับข้าว", text_color=TEXT).pack(pady=(6, 4))
        for count, price in shop["prices"].items():
            ctk.CTkRadioButton(
                parent, text=f"ราด {count} อย่าง — {price} บาท",
                variable=self.dish_count, value=count, command=self.update_price,
                fg_color=ORANGE, hover_color=ORANGE_HOVER,
            ).pack(anchor="w", pady=3)

        ctk.CTkLabel(parent, text="เลือกกับข้าวให้ครบตามจำนวนที่กำหนด", text_color=TEXT).pack(pady=(10, 4))
        self.dish_choices = {}
        for dish in shop["dishes"]:
            choice = ctk.BooleanVar(value=False)
            self.dish_choices[dish] = choice
            ctk.CTkCheckBox(
                parent, text=dish, variable=choice, fg_color=ORANGE, hover_color=ORANGE_HOVER,
            ).pack(anchor="w", pady=3)

        self.extra_rice = ctk.BooleanVar(value=False)
        rice_text = "เพิ่มข้าว"
        if shop["extra_rice_price"] > 0:
            rice_text += f" (+{shop['extra_rice_price']} บาท)"
        ctk.CTkCheckBox(
            parent, text=rice_text, variable=self.extra_rice, command=self.update_price,
            state="normal" if shop.get("extra_rice_available") else "disabled",
            fg_color=ORANGE, hover_color=ORANGE_HOVER,
        ).pack(anchor="w", pady=8)
        self.note_entry = ctk.CTkEntry(parent, placeholder_text="หมายเหตุ เช่น แยกน้ำแกง", height=36)
        self.note_entry.pack(fill="x", pady=6)
        self.price_label = ctk.CTkLabel(
            self.action_area, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color=ORANGE,
        )
        self.price_label.pack(pady=8)
        self.update_price()
        ctk.CTkButton(
            self.action_area, text="เพิ่มลงตะกร้า", height=38, corner_radius=9,
            fg_color=ORANGE, hover_color=ORANGE_HOVER, command=self.add_curry_item,
        ).pack(fill="x", pady=8)

    def update_price(self):
        price = menu.calculate_price(
            self.shop_name, "ข้าวราดแกง", self.dish_count.get(), self.extra_rice.get(),
            menu_data=self.menu_data,
        )
        self.price_label.configure(text=f"ราคาต่อจาน {price} บาท")

    def add_curry_item(self):
        selected_dishes = [dish for dish, choice in self.dish_choices.items() if choice.get()]
        count = self.dish_count.get()
        error = menu.check_selection(self.shop_name, count, selected_dishes, self.menu_data)
        if error:
            self.message_label.configure(text=error)
            return
        price = menu.calculate_price(
            self.shop_name, "ข้าวราดแกง", count, self.extra_rice.get(), menu_data=self.menu_data,
        )
        options = selected_dishes.copy()
        if self.extra_rice.get():
            options.append("เพิ่มข้าว")
        self.add_to_cart(f"ข้าวราดแกง {count} อย่าง", price, options, self.note_entry.get())
        self.message_label.configure(text="เพิ่มข้าวราดแกงลงตะกร้าแล้ว")
        self.update_cart_summary()
