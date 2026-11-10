PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS canteens (
            canteen_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

CREATE TABLE IF NOT EXISTS menu_items (
            menu_id INTEGER PRIMARY KEY,
            shop_id INTEGER NOT NULL REFERENCES shops(shop_id),
            name TEXT NOT NULL,
            price INTEGER NOT NULL CHECK(typeof(price) = 'integer' AND price >= 0),
            is_available INTEGER NOT NULL DEFAULT 1 CHECK(is_available IN (0, 1)),
            menu_type TEXT NOT NULL DEFAULT 'regular',
            dish_count INTEGER,
            image_path TEXT NOT NULL DEFAULT '',
            UNIQUE(shop_id, name)
        );

CREATE TABLE IF NOT EXISTS menu_options (
            option_id INTEGER PRIMARY KEY,
            shop_id INTEGER NOT NULL REFERENCES shops(shop_id),
            group_name TEXT NOT NULL,
            name TEXT NOT NULL,
            extra_price INTEGER NOT NULL CHECK(extra_price >= 0),
            UNIQUE(shop_id, group_name, name)
        );

CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            menu_name TEXT NOT NULL,
            unit_price INTEGER NOT NULL CHECK (unit_price >= 0),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            options TEXT NOT NULL DEFAULT '[]',
            note TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );

CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            canteen_name TEXT NOT NULL,
            shop_name TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            pickup_date TEXT NOT NULL,
            pickup_time TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            request_id TEXT,
            request_payload TEXT,
            is_overdue INTEGER NOT NULL DEFAULT 0
        );

CREATE TABLE IF NOT EXISTS shops (
            shop_id INTEGER PRIMARY KEY,
            canteen_id INTEGER NOT NULL REFERENCES canteens(canteen_id),
            name TEXT NOT NULL,
            shop_type TEXT NOT NULL DEFAULT 'regular',
            opening_time TEXT NOT NULL DEFAULT '06:45',
            closing_time TEXT NOT NULL DEFAULT '16:00',
            slot_capacity INTEGER NOT NULL DEFAULT 10 CHECK(slot_capacity > 0),
            is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
            UNIQUE(canteen_id, name)
        );

CREATE TABLE IF NOT EXISTS menu_variants (
    variant_id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL REFERENCES menu_items(menu_id),
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK(typeof(price) = 'integer' AND price >= 0),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK(is_available IN (0, 1)),
    UNIQUE(menu_id, name)
);

CREATE TABLE IF NOT EXISTS menu_item_options (
    option_id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL REFERENCES menu_items(menu_id),
    group_name TEXT NOT NULL,
    name TEXT NOT NULL,
    extra_price INTEGER NOT NULL DEFAULT 0 CHECK(extra_price >= 0),
    UNIQUE(menu_id, group_name, name)
);
