from playwright.sync_api import expect



def test_add_to_cart(auth_page):
    # Добавляем товар в корзину
    product_cart = auth_page.locator(".inventory_item", has_text="Sauce Labs Bike Light")
    add_button = product_cart.locator("button")     # Кнопка add to card внутри карточки
    add_button.click()

    # Проверяем что кнопка изменилась на Remove
    expect(add_button).to_have_text("Remove")

    # Провеярем счётчик корзины
    expect(auth_page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_sauce_labs_onesie_to_cart(auth_page):
    # Добавляем товар в корзину
    product_cart = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    add_button = product_cart.locator("button")     # Кнопка add to card внутри карточки
    add_button.click()

    # Проверяем что кнопка изменилась на Remove
    expect(add_button).to_have_text("Remove")

    # Провеярем счётчик корзины
    cart_badge = auth_page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    # Удаляем из корзины
    product_cart = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    remove_button = product_cart.locator("button")  # Кнопка add to card внутри карточки
    remove_button.click()

    # Проверяем что кнопка изменилась на Add to cart
    expect(add_button).to_have_text("Add to cart")

    # Провеярем счётчик корзины
    expect(cart_badge).to_have_count(0)


def test_product_details_onesie(auth_page):
    # Добавляем товар в корзину
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")

    # Сохраняем название и цену с карточки
    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()

    # Переходим на страницу товара
    product_card.locator('[data-test="inventory-item-name"]').click()

    # Проверяем название и цену на странице деталей
    detail_name = auth_page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = auth_page.locator('[data-test="inventory-item-price"]').inner_text()

    assert detail_name == product_name, "Название товара не совпадает"
    assert detail_price == product_price, "Цена товара не совпадает"


def test_product_details_onesie_fleece_jacket(auth_page):
    # Добавляем товар в корзину
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Fleece Jacket")

    # Сохраняем название и цену с карточки
    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()

    # Переходим на страницу товара
    product_card.locator('[data-test="inventory-item-name"]').click()

    # Проверяем название и цену на странице деталей
    detail_name = auth_page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = auth_page.locator('[data-test="inventory-item-price"]').inner_text()

    assert detail_name == product_name, "Название товара не совпадает"
    assert detail_price == product_price, "Цена товара не совпадает"


def test_remove_item_from_catalog(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Test.allTheThings() T-Shirt (Red)")
    product_button = product_card.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    product_button.click()

    remove_button = product_card.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]')
    assert remove_button.is_visible(), "Кнопка Remove не появилась"

    remove_button.click()

    add_button = product_card.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
    assert add_button.is_visible(), "Кнопка Add to cart не вернулась после удаления"


def test_remove_onesie_from_catalog(auth_page):
    product_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    product_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    product_button.click()

    remove_button = product_card.locator('[data-test="remove-sauce-labs-onesie"]')
    assert remove_button.is_visible(), "Кнопка Remove не появилась"

    remove_button.click()

    add_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    assert add_button.is_visible(), "Кнопка Add to cart не вернулась после удаления"

