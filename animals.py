import time

from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def sait_parsing():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)

        driver.get("https://moscowzoo.ru/animals/kinds")

        with open("htmlcode.html", "w", encoding="utf-8") as f:  
            f.write(driver.page_source)
        return "сайт обработан"

    except:
        print(f"не удалось обработать сайт")
    finally:
        driver.quit() 

def get_animals():
    """
    Функция, которая получает список названий всех животных с сайта Московского зоопарка.

    Returns:
        Список названий животных.
    """
    try:
        with open("htmlcode.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
    except:
        print("Не получилось обработать bs4")
    
    try:
        animals = soup.find_all(class_="animals-kinds-list__items") 
        
        result = list()

        for item in animals:
            links = item.find_all("a")
            for link in links:
                result.append(link.text.lower())

        return result
    
    except:
        print("Проблема с названиями у животных")
        return []

def get_links():
    """
    Функция, которая получает список ссылок всех животных с сайта Московского зоопарка.

    Returns:
        Список ссылок.
    """
    try:
        with open("htmlcode.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
    except:
        print("Не получилось обработать bs4")

    try:
        animals_list = soup.find_all(class_="animals-kinds-list__items")

        links = list()

        for item in animals_list:
            links_in_item = item.find_all("a")
            for link in links_in_item:
                links.append(link["href"])
        return links
    
    except:
        print("Проблема с ссылками у животных")
        return []

def combine_lists_to_dict(list1, list2):
    """
    Соединяет элементы двух списков попарно в словарь,
    где ключи - элементы из первого списка, а значения - элементы из второго.

    Args:
        list1: Первый список.
        list2: Второй список.

    Returns:
        Словарь, где ключи - элементы из первого списка, а значения - элементы из второго.
    """

    combined_dict = {}
    for i in range(min(len(list1), len(list2))):
        combined_dict[list1[i]] = list2[i]

    return combined_dict

def dict_animals_links():
    try:
        animals = get_animals()
        links = get_links()
        return combine_lists_to_dict(animals,links)
    except:
        print("Произошла ошибка в словаре: животное-ссылка")
        return []

def get_animsls_imgs():
    
    try:
        with open("htmlcode.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
    except:
        print("Не получилось обработать bs4")

    try:
        img_animals = soup.find_all(class_ = "animals-kinds-list__items")

        img_result = list()


        for item in img_animals:
            links_in_item = item.find_all("a")
            for img in links_in_item:
                img_in_a = img.find_all("img")
                for img_link in img_in_a:
                    img_result.append(img_link["src"])
        
        return img_result
    
    except:
        print("Ошибка обработки изображения у животного")
        return []
    
def dict_animal_and_img():
    try:
        imgs = get_animsls_imgs()
        animals = get_animals()
        return combine_lists_to_dict(animals,imgs)
    except:
        print("Не удалось получить словарь животное-изображение")
        return []

def who_info(text_from_p: str):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        driver.get(f"https://ru.wikipedia.org/wiki/{text_from_p.capitalize()}")
        
        try:
            wait = WebDriverWait(driver, 1)
            get_info = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/p[1]"))).text 
        except (TimeoutException, NoSuchElementException):
            get_info = "Описание на сайте не найдено."
            
        driver.quit()
        
        return get_info
    except TimeoutException:
        print("Не удалось загрузить страницу")
    except ConnectionError:
        print("Проблемы с подключением к сети")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def html_save_animals():
    animals_and_links = dict_animals_links()  

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    for animal, link in animals_and_links.items():
        try:
            
            driver.get("https://moscowzoo.ru" + link)
            time.sleep(1)
            
            filename = f"{animal.lower()}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            print(f"Сохранено: {filename}")
        
        except Exception as e:
            print(f"Ошибка при обработке {animal}: {e}")
    print("Все существа загружены")
    driver.quit()

def get_info_animals(animal: str) -> str:
    animals = get_animals()
    animal = animal.lower()  # Исправлено: нужно присвоить результат `lower()`

    if animal in animals:
        try:
            with open(f"{animal}.html", "r", encoding="utf-8") as f:
                animal_html = f.read()
            soup = BeautifulSoup(animal_html, "html.parser")
        except FileNotFoundError:
            print(f"Файл {animal}.html не найден.")
            return ""
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return ""

        result = []
        systematics_found = False
        areal_found = False

        # Проверяем наличие систематики и ареала на странице
        for tag in soup.find_all(class_="systematics"):
            if not systematics_found:
                systematics_text = tag.text.replace("Систематика:", "").strip()  # Удаляем "Систематика:"
                result.append(f"{systematics_text}")  # Без "Систематика:\n"
                systematics_found = True

        for tag in soup.find_all(class_="areal"):
            if not areal_found:
                areal_text = tag.text.replace("Ареал:", "").strip()  # Удаляем "Ареал:"
                result.append(f"{areal_text}")  # Без "Ареал:\n"
                areal_found = True

        description_added = False
        for tag in soup.find_all(class_="text-block"):
            if not description_added:
                result.append("Описание:")
                description_added = True
            result.append(tag.text)

        return "\n".join(result)
    else:
        print("В списке нет такого животного")
        return ""


if __name__ == "__main__":
    pass