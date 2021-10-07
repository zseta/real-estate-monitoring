# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import Compose, TakeFirst, Identity, MapCompose
from scrapy import Field, Item
from w3lib.html import remove_tags

def is_flat(parameter_list):
    return len(parameter_list) == 3
    
def clean_price(value_list):
    value_raw = remove_tags(value_list[0])
    value = value_raw.replace("Ft", "").replace(",", ".").replace("€", "").replace(" ", "")
    if "millió" in value:
        value = value.replace("millió", "").strip()
        value = int(float(value)*1000000)
    elif "ezer" in value:
        value = value.replace("ezer", "").strip()
        value = int(float(value)*1000)
    elif "milliárd" in value:
        return None
    
    if "€" in value_raw:
        value = value * 360
    return value

def clean_area(value_list):
    value = remove_tags(value_list[1])
    return int(value[:value.find("m")-1].replace(" ", ""))

def clean_area_lot(value_list):
    if is_flat(value_list):
        return None
    value = remove_tags(value_list[-2])
    return int(value[:value.find("m")-1].replace(" ", ""))

def clean_rooms(value_list):
    value = remove_tags(value_list[-1]).replace("fél", "").strip()
    if "+" in value:
        values = value.replace(" ", "").split("+")
        return int(values[0])+int(values[1])
    return int(value)

def clean_building_floors(value):
    value = value.strip()
    if "nincs megadva" in value:
        return None
    elif "földszint" in value or "félemelet" in value:
        return 0
    elif "10 felett" in value or "több mint 10" in value:
        return 11
    elif "szuterén" in value:
        return -1        
    return int(value.strip())

def clean_property_type(value):
    value = value.strip()
    if "Eladó panel lakás" == value:
        return "panel"
    elif "Eladó tégla építésű lakás" == value:
        return "tégla lakás"
    elif "Tégla építésű lakás bérleti joga átadó" == value or "Panel lakás bérleti joga átadó" == value:
        return "bérleti jog"
    elif "csúszózsalus" in value:
        return "csúszózsalus"
    elif "lakóparkban" in value:
        return "lakópark"
    elif "Eladó ikerház" == value:
        return "ikerház"
    elif "Eladó sorház" == value:
        return "sorház"
    elif "Eladó családi ház" == value:
        return "családi ház"
    elif "Eladó házrész" == value:
        return "házrész"
    elif "Eladó könnyűszerkezetes ház" == value:
        return "könnyűszerkezetes ház"
    return value.replace("Eladó", "").strip()

def clean_build_year(value):
    if "nincs megadva" in value:
        return None    
    return value.strip()
    
def clean_property_condition(value):
    if "nincs megadva" in value:
        return None
    return value.strip()

class RealEstateItem(Item):
    url = Field()
    city = Field(
        input_processor=MapCompose(remove_tags, lambda value: value.split(",")[0].strip()),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(remove_tags, lambda value: value.split(",")[1].strip() if len(value.split(","))>1 else None),
        output_processor=TakeFirst()
    )
    area = Field(
        input_processor=Compose(clean_area),
        output_processor=TakeFirst()
    )
    area_lot = Field(
        input_processor=Compose(clean_area_lot),
        output_processor=TakeFirst()
    )
    rooms = Field(
        input_processor=Compose(clean_rooms),
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=Compose(clean_price),
        output_processor=TakeFirst()
    )
    property_condition = Field(
        input_processor=MapCompose(remove_tags, clean_property_condition)
    )
    build_year = Field(
        input_processor=MapCompose(remove_tags, clean_build_year)
    )
    description = Field()
    floor = Field(
        input_processor=MapCompose(remove_tags, clean_building_floors)
    )
    building_floors = Field(
        input_processor=MapCompose(remove_tags, clean_building_floors)
    )
    property_type = Field(
        input_processor=MapCompose(remove_tags, clean_property_type)
    )
    advertiser_agent = Field(
        input_processor=MapCompose(remove_tags, lambda value: value.strip())
    )
    advertiser_name = Field(
        input_processor=MapCompose(remove_tags, lambda value: value.strip())
    )
    time = Field(
        input_processor=Identity(),
        output_processor=TakeFirst()
    )
    

class RealEstateUrlItem(Item):
    url = Field()
    city = Field()