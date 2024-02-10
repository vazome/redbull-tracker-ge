import prettytable as pt

a = [
    ("Energy Drunk Red Bull 250ml", 3.99, "Zgapari Dighomi", "wolt"),
    ("Energy Drunk Red Bull sugar free 250ml", 3.99, "Zgapari Dighomi", "wolt"),
    ("Energy Drunk Red Bull 250ml", 3.99, "Zgapari Saburtalo", "wolt"),
    (
        "რედ ბული უშაქრო ენერგეტიკული სასმელი 250 მლ/90162800 1ც",
        4.2,
        "Carrefour Dighomi Massive",
        "wolt",
    ),
    (
        "რედ ბული ენერგეტიკული სასმელი ტროპიკი 250 მლ/90435201 1ც",
        4.2,
        "Carrefour Dighomi Massive",
        "wolt",
    ),
    (
        "რედ ბული ენერგეტიკული სასმელი ტროპიკი 250 მლ/90435201 1ც",
        4.2,
        "Carrefour",
        "glovo",
    ),
    ("რედ ბული ენერგეტიკული სასმელი 250 მლ/90162718 1ც", 4.2, "Carrefour", "glovo"),
    (
        "რედ ბული ენერგეტიკული სასმელი 250 მლ/90162718 1ც",
        4.2,
        "Carrefour Dighomi Massive",
        "wolt",
    ),
    (
        "რედ ბული უშაქრო ენერგეტიკული სასმელი 250 მლ/90162800 1ც",
        4.2,
        "Carrefour",
        "glovo",
    ),
    (
        "რედ ბული ენერგეტიკული სასმელი 250 მლ/90162718 1ც",
        4.2,
        "Carrefour Eristavi",
        "wolt",
    ),
]

table_header = (
    f"{'Product':<40} | {'Price':<5} | {'Venue':<20} | {'Platform':<10}\n" + "-" * 90
)
table_rows = [table_header]
for item in a:
    product_name, product_price, venue_name, platform_name = item
    row = f"{product_name:<40} | {product_price:<5} | {venue_name:<20} | {platform_name:<10}"
    table_rows.append(row)

table_str = "\n".join(table_rows)

print(table_str)


def send_table(data):
    table = pt.PrettyTable(["Product", "Price", "Venue", "Platform"])
    table.align["Product"] = "l"
    table.align["Price"] = "r"
    table.align["Venue"] = "l"
    table.align["Platform"] = "l"
    for product, price, venue, platform in data:
        table.add_row(
            [
                product.replace("Energy Drink", "")
                .replace("ენერგეტიკული", "")
                .replace("Energy Drunk", "")
                .replace("სასმელი", ""),
                f"{price:.2f}",
                venue,
                platform,
            ]
        )
    return table


print(send_table(a))
