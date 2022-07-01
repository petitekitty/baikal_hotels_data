import time
import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import numpy as np

hotel_list = []

def get_data(url, html_selector_value):
    service = ''
    good_review = ''
    bad_review = ''
    driver = webdriver.Chrome(service=Service('C:\\Users\\lynnk\\PycharmProjects\\hotels\\chromedriver.exe'))
    driver.get(url=url)
    try:
        driver.execute_script("arguments[0].click();", driver.find_element(by=By.CLASS_NAME, value='zenreactformoverlay-close'))
    except:
        pass
    time.sleep(1)
    hotel_name = driver.find_elements(by=By.CLASS_NAME, value=html_selector_value[0])
    hotel_page = driver.find_elements(by=By.CLASS_NAME, value=html_selector_value[1])
    hotel_price = driver.find_elements(by=By.CLASS_NAME, value=html_selector_value[2])
    hotel_address = driver.find_elements(by=By.CLASS_NAME, value=html_selector_value[11])
    for i in range(len(hotel_name)):
        try:
            page = hotel_page[i].get_attribute('href')
        except:
            page = np.nan
        try:
            name = hotel_name[i].text
        except:
            name = np.nan
        try:
            price_elements = hotel_price[i].text.split('₽')
            price = price_elements[0].split('от')
            min_price = ''.join(price)

        except:
            min_price = np.nan
        try:
            address_elements = hotel_address[i].text.split(', ')
            city = address_elements[-1]
        except:
            city = np.nan
        driver_for_page = webdriver.Chrome(service=Service('C:\\Users\\lynnk\\PycharmProjects\\hotels\\chromedriver.exe'))
        driver_for_page.get(url=page)
        try:
            driver_for_page.execute_script("arguments[0].click();", driver_for_page.find_element(by=By.CLASS_NAME, value='zenreactformoverlay-close'))
        except:
            pass
        time.sleep(1)
        try:
            address = driver_for_page.find_element(by=By.CLASS_NAME, value=html_selector_value[3]).text
        except:
            address = np.nan
        global mirturbaz_selector_value
        if html_selector_value == mirturbaz_selector_value:
            try:
                distance = float(driver_for_page.find_element(by=By.ID, value=html_selector_value[4]).text[:-3])
            except:
                distance = np.nan
        else:
            try:
                distance = float(driver_for_page.find_element(by=By.CLASS_NAME, value=html_selector_value[4]).text[:-3])
            except:
                distance = np.nan
        hotel_service = driver_for_page.find_elements(by=By.CLASS_NAME, value=html_selector_value[5])
        for i in range(len(hotel_service)):
            try:
                service += hotel_service[i].text + '; '
            except:
                service = np.nan
        try:
            rating_elements = driver_for_page.find_element(by=By.CLASS_NAME, value=html_selector_value[6]).text.split('/')
            rating = float(rating_elements[0])
        except:
            rating = np.nan
        try:
            driver_for_page.execute_script("arguments[0].click();", driver_for_page.find_element(by=By.CLASS_NAME, value='zenroomspagereviews-button-expand'))
        except:
            pass
        time.sleep(1)
        try:
            open_review = driver_for_page.find_elements(by=By.CLASS_NAME, value='zen-spoiler-label')
            for i in range(len(open_review)):
                driver_for_page.execute_script("arguments[0].click();", driver_for_page.find_element(by=By.CLASS_NAME, value='zen-spoiler-label'))
        except:
            pass
        time.sleep(1)
        hotel_good_review = driver_for_page.find_elements(by=By.CLASS_NAME, value=html_selector_value[7])
        hotel_bad_review = driver_for_page.find_elements(by=By.CLASS_NAME, value=html_selector_value[8])
        for i in range(len(hotel_good_review)):
            try:
                good_review += hotel_good_review[i].find_element(by=By.CLASS_NAME, value=html_selector_value[9]).text + '; '
            except:
                good_review = np.nan
        for i in range(len(hotel_bad_review)):
            try:
                bad_review += hotel_bad_review[i].find_element(by=By.CLASS_NAME, value=html_selector_value[10]).text + '; '
            except:
                bad_review = np.nan
        hotel_list.append(
            {
                'name': name,
                'url': page,
                'address': address,
                'city': city,
                'min_price, RUB': min_price,
                'distance, km': distance,
                'service': service,
                'rating': rating,
                'good_review': good_review,
                'bad_review': bad_review
            }
        )
        service = ''
        good_review = ''
        bad_review = ''
    return hotel_list


def make_table(hotel_list):
    data = pandas.DataFrame(hotel_list)
    print(data)
    city_pivot = pandas.pivot_table(data, index=['city'], values=["name"], aggfunc={'name': len})
    print(city_pivot)
    data.to_csv('data.csv')
    city_pivot.to_csv('city_pivot.csv')
    return data, city_pivot


url_mirturbaz = 'https://mirturbaz.ru/russia/water/ozero-baykal?page={}'
mirturbaz_selector_value = ['card__title', 'card__price-btn', 'card__price', 'camp_full_address',
                       'camp_to_area_center_distance', 'base-services-box-row__title', 'card__rating-numb',
                       'review-list-item__text-plus', 'review-list-item__text-minus', 'review-list-item__text-par',
                       'review-list-item__text-par', 'card__contact-item-link']
url_ostrovok = 'https://ostrovok.ru/hotel/russia/baykal/?q=6307686&guests=1&page={}&price=one&sid=19ee1388-d9ac-427f-a659-169c4a056d84'
ostrovok_selector_value = ['zen-hotelcard-name', 'zen-hotelcard-name-link', 'zen-hotelcard-rate-price-value',
                           'zenroomspagelocation-address', 'zenroomspagelocation-distance-value', 'zenroomspageperks-amenities-item',
                           'zenroomspageperks-rating-info-total-value', 'zenroomspagehotelreviewcontent-reviews', 'zenroomspagehotelreviewcontent-reviews',
                           'zenroomspagehotelreviewcontent-plus-description', 'zenroomspagehotelreviewcontent-minus-description', 'zen-hotelcard-address']


site_selection = input('Выберите сайт для сбора данных из списка и введите его номер.\n1)Островок.ру\n2)Мир турбаз\n', )
if site_selection == '1':
    print('Пожалуйста, подождите, идёт сбор данных!')
    for page in range(1, 23):
        url = url_ostrovok.format(page)
        get_data(url, ostrovok_selector_value)
    make_table(hotel_list)
    print('Данные успешно получены!')
elif site_selection == '2':
    print('Пожалуйста, подождите, идёт сбор данных!')
    for page in range(1, 11):
        url = url_mirturbaz.format(page)
        get_data(url, mirturbaz_selector_value)
    make_table(hotel_list)
    print('Данные успешно получены!')
else:
    print('Извините, но пока мы не можем собрать данные с этого сайта')
