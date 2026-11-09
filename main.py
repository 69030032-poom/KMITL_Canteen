import argparse

import customtkinter as ctk

from Frontend.app import CanteenApp


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    parser = argparse.ArgumentParser()
    parser.add_argument('--role', choices=['customer', 'shop'], default='customer')
    args = parser.parse_args()
    app = CanteenApp(role=args.role)
    app.mainloop()


if __name__ == "__main__":
    main()
