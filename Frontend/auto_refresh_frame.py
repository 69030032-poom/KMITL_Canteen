import sqlite3
import customtkinter as ctk
from Backend import database


class AutoRefreshFrame(ctk.CTkFrame):
    """อ่านสถานะใหม่เมื่อฐานข้อมูลเปลี่ยน โดยตรวจทุก 3 วินาที"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.refresh_page = None
        self.refresh_paused = False
        self.refresh_connection = database.connect_database()
        self.data_version = self.read_version()
        self.refresh_timer = self.after(3000, self.check_for_updates)

    def read_version(self):
        return self.refresh_connection.execute('PRAGMA data_version').fetchone()[0]

    def check_for_updates(self):
        self.refresh_timer = None
        try:
            if not self.refresh_paused:
                version = self.read_version()
                if version != self.data_version and self.refresh_page:
                    if self.refresh_page() is not False:
                        self.data_version = version
        except (sqlite3.Error, ValueError):
            pass  # ลองใหม่รอบถัดไปเมื่อฐานข้อมูลกลับมาอ่านได้
        self.refresh_timer = self.after(3000, self.check_for_updates)

    def destroy(self):
        if self.refresh_timer is not None:
            self.after_cancel(self.refresh_timer)
            self.refresh_timer = None
        self.refresh_connection.close()
        super().destroy()
