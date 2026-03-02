import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    date_time_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', content)
    date = date_time_match.group(1) if date_time_match else None
    time = date_time_match.group(2) if date_time_match else None

    payment_match = re.search(r'(Банковская карта|Наличные):', content)
    payment_method = payment_match.group(1) if payment_match else "Unknown"

    total_match = re.search(r'ИТОГО:\s*([\d\s]+,\d{2})', content)
    total_amount = total_match.group(1).replace(' ', '') if total_match else "0,00"

    product_pattern = re.compile(
        r'(\d+)\.\n(.*?)\n(?:\\s*)?(\d+,\d{0,3}\s*x\s*[\d\s,]+)\n([\d\s,]+)\nСтоимость\n([\d\s,]+)',
        re.DOTALL
    )

    products = []
    all_prices = []

    for match in product_pattern.finditer(content):
        name = match.group(2).strip().replace('\n', ' ')
        price_per_unit = match.group(4).strip().replace(' ', '')
        total_item_price = match.group(5).strip().replace(' ', '')
        
        products.append(name)
        all_prices.append(total_item_price)
        
    parsed_data = {
        "metadata": {
            "date": date,
            "time": time,
            "payment_method": payment_method,
            "total_calculated": total_amount
        },
        "items": [
            {"name": n, "price": p} for n, p in zip(products, all_prices)
        ]
    }

    return parsed_data

if __name__ == "__main__":
    result = parse_receipt('raw.txt')
    print(json.dumps(result, indent=4, ensure_ascii=False))