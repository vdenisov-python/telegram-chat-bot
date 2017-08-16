import re
import requests
import random


def search_by_keyword(word):
    main_url = "https://yandex.ru/images/search?text="
    category_images = word
    data = requests.get(main_url + category_images)
    pattern = r"http:[\w, \., \_, \-, \/, \:]*jpg"
    all_images = re.findall(pattern, data.text)
    random_image = random.choice(all_images)
    return random_image
