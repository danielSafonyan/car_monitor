def strip_price(price: str):
    chars = ['€', ',', '-']
    for ch in chars:
        price = price.replace(ch, '')
    return float(price)

def strip_km(price: str):
    chars = [' km', ',']
    for ch in chars:
        price = price.replace(ch, '')
    return float(price)


res = strip_km('38,251 km')
print(res)