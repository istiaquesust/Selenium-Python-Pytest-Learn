# run command on terminal to go directory -> cd code
# then run command -> pytest -s -v TestCaseForSauceDemoSite.py

import platform
import pytest
from selenium import webdriver


class TestSauceDemo:

    def setup(self):
        if 'Windows' in platform.system():  # windows
            path = '../drivers/chromedriver.exe'
        else:
            path = '../drivers/chromedriver'
        url = 'https://www.saucedemo.com/'
        self.driver = webdriver.Chrome(path)
        self.driver.get(url)
        self.driver.maximize_window()
        self.price = []
        self.products = []
        self.total_price = 0
        self.search_product_number = 0

    def teardown(self):
        self.driver.quit()

    def test_order_min_priced_product(self):
        self.driver.find_element_by_css_selector('#user-name').send_keys('standard_user')
        self.driver.find_element_by_css_selector('#password').send_keys('secret_sauce')
        self.driver.find_element_by_css_selector('#login-button').click()
        success_login_expected_url = 'https://www.saucedemo.com/inventory.html'
        assert self.driver.current_url.__contains__(success_login_expected_url)

        # get min priced product position and click add to cart
        list_products = self.get_products()
        min_priced_product = min(list_products, key=lambda x: x['price'])
        min_priced_product_position = list_products.index(min_priced_product) + 1
        add_to__cart_xpath = '//*[@id="inventory_container"]/div/div[' + str(
            min_priced_product_position) + ']/div[3]/button'
        self.driver.find_element_by_xpath(add_to__cart_xpath).location_once_scrolled_into_view
        self.driver.find_element_by_xpath(add_to__cart_xpath).click()
        self.total_price = min_priced_product['price']

        # order product
        if self.total_price is not 0:
            self.order_product()

    def test_order_products_with_name(self):
        self.driver.find_element_by_css_selector('#user-name').send_keys('standard_user')
        self.driver.find_element_by_css_selector('#password').send_keys('secret_sauce')
        self.driver.find_element_by_css_selector('#login-button').click()
        success_login_expected_url = 'https://www.saucedemo.com/inventory.html'
        assert self.driver.current_url.__contains__(success_login_expected_url)

        # get products position and click add to cart
        list_products = self.get_products()
        search_products = self.search_products()
        if len(search_products) <= len(list_products):
            for i in range(len(search_products)):
                for j in range(len(list_products)):
                    my_dictionary = list_products[j]
                    if search_products[i] in my_dictionary['name']:
                        self.total_price += my_dictionary['price']
                        product_position = j + 1
                        add_to__cart_xpath = '//*[@id="inventory_container"]/div/div[' + str(
                            product_position) + ']/div[3]/button'
                        self.driver.find_element_by_xpath(add_to__cart_xpath).location_once_scrolled_into_view
                        self.driver.find_element_by_xpath(add_to__cart_xpath).click()
                        break
        # order product
        if self.total_price is not 0:
            self.order_product()

    # load product name and price in a list of dictionaries
    def get_products(self):
        # get product name and price from element
        product_elements = self.driver.find_elements_by_class_name('inventory_item_name')
        price_elements = self.driver.find_elements_by_class_name('inventory_item_price')

        # Load name and prices in a List of dictionaries
        for price_element, product_element in zip(price_elements, product_elements):
            price_with_sign = str(price_element.text)
            price_without_sign = price_with_sign.replace('$', '')
            my_dictionary = {'name': str(product_element.text), 'price': float(price_without_sign)}
            self.products.append(my_dictionary)

        return self.products

    # set products to order
    def search_products(self):
        products_to_order = ['Jacket', 'Bike Light', 'nothing']
        return products_to_order

    def order_product(self):
        # order product
        self.driver.find_element_by_class_name('shopping_cart_container').click()
        self.driver.find_element_by_link_text('CHECKOUT').click()
        self.driver.find_element_by_id('first-name').send_keys('John')
        self.driver.find_element_by_id('last-name').send_keys('Doye')
        self.driver.find_element_by_id('postal-code').send_keys('12525')
        self.driver.find_element_by_css_selector('.cart_button').click()
        compare_price = str(self.driver.find_element_by_class_name('summary_subtotal_label').text)

        # if selected product price and sub-total price is same, click finish.
        assert str(self.total_price) in compare_price
        self.driver.find_element_by_link_text('FINISH').location_once_scrolled_into_view
        self.driver.find_element_by_link_text('FINISH').click()

        # If Success page arrives, pass
        assert 'Finish' in self.driver.page_source
