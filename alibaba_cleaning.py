import re

def cleaning(villa_info):
    data = {}
  
    # Villa Name
    match = re.search(r"Villa Name:\s*(.*)", raw_text)
    data['name'] = match.group(1).strip() if match else ""

    # Price
    match = re.search(r"Villa Price:\s*([\d,]+)", raw_text)
    data['price_per_night'] = int(match.group(1).replace(',', '')) if match else 0

    # Features
    match = re.search(r"Functionality:\s*(.*?)Headers:", raw_text, re.DOTALL)
    if match:
        functionalities = match.group(1).strip().split(',')
        data['features'] = [f.strip() for f in functionalities if f.strip()]
    else:
        data['features'] = []

    # Headers
    match = re.search(r"Headers:\s*(.*?)Villa Info:", raw_text, re.DOTALL)
    data['headers'] = match.group(1).strip() if match else ""

    # Description
    match = re.search(r"Villa Info:\s*(.*?)(={5,}|$)", raw_text, re.DOTALL)
    data['description'] = match.group(1).strip() if match else ""

    return data


# example:
"""
Villa Name: اجاره ویلا فلت دفراز توتکابن
Villa Price: 3,500,000
Functionality: 
آب , برق , گاز , سیستم سرمایشی , سیستم گرمایشی , مبلمان , تلویزیون , گیرنده دیجیتال ایران , جالباسی , سرویس بهداشتی ایرانی , حمام , آشپزخانه , یخچال , اجاق گاز , وسایل پخت و پز , لوازم سرو غذا , 
Headers: 
بدون اتاق , 1 تخت دو نفره , 3 رخت‌خواب سنتی , لغو رزرو بدون جریمهامکان لغو رزرو از سمت مهمان تا 10 روز قبل از شروع سفر فقط در تعطیلات و روز‌های پرتقاضا , امکان پرداخت اقساطیپرداخت اقساطی بدون نیاز به ضامن و مراجعه حضوری , 
Villa Info: 
اقامتگاه در محیطی آرام، ویلایی و بومی واقع است.
ویلا به صورت غیردربست و حیاطو بالکن اشتراکی می باشد.
برای پارک 3 خودرو پارکینگ روباز دارد. 
قابل توجه مهمانان همراه با سالمند، کودک و افراد دارای معلولیت، این اقامتگاه در طبقه همکف و دارای 6 پله می باشد.
بافت محله روستایی و دسترسی به اقامتگاه آسفالت می باشد.
فاصله تا جنگل 5دقیقه، دریا 1 ساعت، سوپرمارکت 2دقیقه، و نانوایی 5دقیقه می باشد.
اقامتگاه قبل از ورود مهمان بطور کامل نظافت خواهد شد.
====================================================================================================

"""
