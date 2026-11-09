import sqlite3

import customtkinter as ctk

from Backend import users


# KMITL Canteen login/register page
# Keeps the existing Backend authentication and registration calls.
ORANGE = "#F45B2A"
ORANGE_HOVER = "#DF4B20"
TEXT = "#242424"
MUTED = "#777777"
BORDER = "#E7E7E7"
WHITE = "#FFFFFF"
SOFT_BG = "#FFF7F3"
ERROR = "#C62828"
SUCCESS = "#237A45"


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login, role="customer"):
        super().__init__(parent, fg_color="transparent")
        self.on_login = on_login
        self.role = role
        self.register = False
        self._build_layout()
        self.show_form()

    def _build_layout(self):
        # Center the login card while allowing it to resize with the main window.
        self.grid_columnconfigure(0, weight=1)

        self.hero = ctk.CTkFrame(self, fg_color=SOFT_BG, corner_radius=18, border_width=1,
                                 border_color="#FFE5D9")
        self.hero.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 18))
        self.hero.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.hero,
            text="กินอร่อย สั่งง่าย ในรั้ว สจล.",
            font=ctk.CTkFont(size=14),
            text_color=MUTED,
        ).pack(pady=(18, 5))
        ctk.CTkLabel(
            self.hero,
            text="ยินดีต้อนรับสู่โรงอาหาร KMITL",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=TEXT,
        ).pack(pady=(0, 18))

        self.card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=18,
                                 border_width=1, border_color=BORDER)
        self.card.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 16))
        self.card.grid_columnconfigure(0, weight=1)

        self.form_content = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_content.pack(fill="x", padx=28, pady=24)
        self.form_content.grid_columnconfigure(0, weight=1)

    def _make_entry(self, parent, label_text, placeholder, password=False):
        field = ctk.CTkFrame(parent, fg_color="transparent")
        field.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(
            field,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 6))
        entry = ctk.CTkEntry(
            field,
            height=42,
            corner_radius=9,
            border_width=1,
            border_color=BORDER,
            fg_color="#FFFFFF",
            text_color=TEXT,
            placeholder_text=placeholder,
            show="*" if password else "",
        )
        entry.pack(fill="x")
        return entry

    def choose_role(self, value):
        self.role = 'shop' if value == 'ร้านค้า' else 'customer'
        self.show_form()

    def show_form(self, register=False):
        for widget in self.form_content.winfo_children():
            widget.destroy()

        if self.role == 'shop':
            register = False
        self.register = register
        self.role_picker = ctk.CTkSegmentedButton(
            self.form_content, values=['ลูกค้า', 'ร้านค้า'], command=self.choose_role,
            selected_color=ORANGE, selected_hover_color=ORANGE_HOVER,
        )
        self.role_picker.set('ร้านค้า' if self.role == 'shop' else 'ลูกค้า')
        self.role_picker.pack(fill='x', pady=(0, 12))
        title = "สร้างบัญชีใหม่" if register else ("เข้าสู่ระบบร้านค้า" if self.role == "shop" else "เข้าสู่ระบบลูกค้า")
        subtitle = (
            "สมัครสมาชิกเพื่อเริ่มสั่งอาหารจากร้านโปรด"
            if register else "เข้าสู่ระบบเพื่อสั่งอาหารได้สะดวกยิ่งขึ้น"
        )

        ctk.CTkLabel(
            self.form_content,
            text=title,
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT,
        ).pack(pady=(0, 4))
        ctk.CTkLabel(
            self.form_content,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=MUTED,
        ).pack(pady=(0, 12))

        self.username_entry = self._make_entry(
            self.form_content, "ชื่อผู้ใช้", "กรอกชื่อผู้ใช้"
        )
        self.password_entry = self._make_entry(
            self.form_content, "รหัสผ่าน", "รหัสผ่าน 8–128 ตัวอักษร", password=True
        )

        if register:
            self.confirm_entry = self._make_entry(
                self.form_content, "ยืนยันรหัสผ่าน", "กรอกรหัสผ่านอีกครั้ง", password=True
            )
            self.name_entry = self._make_entry(
                self.form_content, "ชื่อที่แสดงในแอป", "ชื่อของคุณ"
            )

        self.error_label = ctk.CTkLabel(
            self.form_content,
            text="",
            text_color=ERROR,
            font=ctk.CTkFont(size=12),
            wraplength=420,
        )
        self.error_label.pack(fill="x", pady=(8, 2))

        self.submit_button = ctk.CTkButton(
            self.form_content,
            text="สมัครสมาชิก" if register else "เข้าสู่ระบบ",
            command=self.submit,
            height=44,
            corner_radius=10,
            fg_color=ORANGE,
            hover_color=ORANGE_HOVER,
            text_color=WHITE,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.submit_button.pack(fill="x", pady=(8, 10))

        switch_text = "มีบัญชีอยู่แล้ว? เข้าสู่ระบบ" if register else "ยังไม่มีบัญชี? สมัครสมาชิก"
        self.switch_button = ctk.CTkButton(
            self.form_content,
            text=switch_text,
            command=lambda: self.show_form(not register),
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color=SOFT_BG,
            border_width=1,
            border_color="#FFD2C1",
            text_color=ORANGE,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        if self.role == 'customer':
            self.switch_button.pack(fill="x")
        else:
            ctk.CTkLabel(self.form_content, text='ใช้บัญชีร้านค้าที่ผู้ดูแลสร้างและผูกกับร้านไว้',
                         text_color=MUTED).pack(pady=6)

        self.username_entry.bind("<Return>", lambda _event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda _event: self.submit())
        self.username_entry.focus_set()

    def submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="กรุณากรอกชื่อผู้ใช้และรหัสผ่าน", text_color=ERROR)
            return

        self.submit_button.configure(state="disabled")
        try:
            if self.register:
                if password != self.confirm_entry.get():
                    raise ValueError("รหัสผ่านทั้งสองช่องไม่ตรงกัน")
                users.register_customer(username, password, self.name_entry.get().strip())
                self.show_form(register=False)
                self.username_entry.insert(0, username)
                self.error_label.configure(
                    text="สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ",
                    text_color=SUCCESS,
                )
                return

            user = users.login(username, password)
            if user['role'] != self.role:
                users.logout()
                raise ValueError('บัญชีนี้เป็นบัญชีร้านค้า กรุณาเลือกฝั่งร้านค้า' if user['role'] == 'shop'
                                 else 'บัญชีนี้เป็นบัญชีลูกค้า กรุณาเลือกฝั่งลูกค้า')
        except ValueError as error:
            self.error_label.configure(text=str(error), text_color=ERROR)
        except sqlite3.Error as error:
            print("DATABASE ERROR:", repr(error))
            self.error_label.configure(
                text="เปิดข้อมูลบัญชีไม่ได้ กรุณาตรวจสอบฐานข้อมูลแล้วลองใหม่",
                text_color=ERROR,
            )
        else:
            self.on_login(user)
            return

        self.submit_button.configure(state="normal")
