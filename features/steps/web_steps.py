from behave import when, then
from selenium.webdriver.common.by import By

@when('I visit the "{page_name}"')
def step_impl(context, page_name):
    """Navigasi ke halaman utama aplikasi"""
    if page_name == "Home Page":
        context.driver.get(context.base_url)

@when('I set the "{field_name}" to "{value}"')
def step_impl(context, field_name, value):
    """Mengisi kolom teks input berdasarkan ID elemen HTML"""
    element_id = field_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(value)

@when('I select "{value}" from the "{dropdown_name}" dropdown')
def step_impl(context, value, dropdown_name):
    """Memilih opsi dari sebuah dropdown menu"""
    element_id = dropdown_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.send_keys(value)

@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    """Menekan tombol aksi"""
    button_id = button_name.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()

@when('I copy the "{field_name}" element')
def step_impl(context, field_name):
    """Menyalin teks dari suatu kolom (misal menyalin Id Produk) untuk dipakai nanti"""
    element_id = field_name.lower().replace(" ", "_")
    context.copied_data = context.driver.find_element(By.ID, element_id).get_attribute("value")

@when('I paste the "{field_name}" element')
def step_impl(context, field_name):
    """Menempelkan kembali teks yang sudah disalin ke dalam kolom baru"""
    element_id = field_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(context.copied_data)

@then('I should see the message "{message}"')
def step_impl(context, message):
    """Memverifikasi pesan kilat/flash message di atas layar"""
    element = context.driver.find_element(By.ID, "flash_message")
    assert message in element.text

@then('I should see "{value}" in the "{field_name}" field')
def step_impl(context, value, field_name):
    """Memverifikasi isi data dari sebuah input field"""
    element_id = field_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert value in element.get_attribute("value")

@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Memverifikasi data tabel pencarian mengandung teks tertentu"""
    element = context.driver.find_element(By.ID, "search_results")
    assert text in element.text

@then('I should NOT see "{text}" in the results')
def step_impl(context, text):
    """Memverifikasi data tabel pencarian TIDAK mengandung teks tertentu"""
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text