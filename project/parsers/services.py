# test_spbu.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback
#
# def parse_spbu():
#     url = (
#         'https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list'
#         '&education_level_sort_order=1'
#         '&speciality=09.03.03%7C%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0'
#         '&program_name=%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82+%D0%B8+%D0%BD%D0%B0%D1%83%D0%BA%D0%B0+%D0%BE+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85'
#         '&education_form_name=&fin_source_name=&faculty_name=&is_foreign=0'
#     )
#
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--window-size=1920,1080')
#     options.add_argument('--no-sandbox')
#
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#
#     try:
#         print("⏳ Открываем страницу...")
#         driver.get(url)
#
#         # Ждём, пока появится заголовок "Сумма конкурсных баллов"
#         wait = WebDriverWait(driver, 20)
#         header = wait.until(EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Сумма конкурсных баллов')]")))
#         table = header.find_element(By.XPATH, "./ancestor::table")
#         print("✅ Найдена таблица с абитуриентами")
#
#         # --- Мета-информация ---
#         direction = program = budget = None
#         for elem in driver.find_elements(By.XPATH, "//*[contains(text(), 'Направление подготовки:')]"):
#             direction = elem.text.strip()
#         for elem in driver.find_elements(By.XPATH, "//*[contains(text(), 'Образовательная программа:')]"):
#             program = elem.text.strip()
#         for elem in driver.find_elements(By.XPATH, "//*[contains(text(), 'Количество бюджетных мест:')]"):
#             budget = elem.text.strip()
#
#         print("\n📌 Направление:", direction)
#         print("📌 Программа:", program)
#         print("📌 Бюджетных мест:", budget)
#
#         # --- Парсим строки таблицы ---
#         rows = table.find_elements(By.TAG_NAME, 'tr')
#         print(f"\n📋 Всего строк в таблице (включая заголовок): {len(rows)}")
#         if len(rows) < 2:
#             print("⚠️ Таблица пуста")
#             return
#
#         data_rows = rows[1:]  # пропускаем заголовок
#         print(f"📋 Строк с данными: {len(data_rows)}")
#
#         # Собираем баллы (третий столбец, индекс 2)
#         scores = []
#         print("\n📋 Данные всех строк:")
#         for row in data_rows:
#             cols = row.find_elements(By.TAG_NAME, 'td')
#             if len(cols) >= 3:
#                 num = cols[0].text.strip()
#                 code = cols[1].text.strip()
#                 score_str = cols[2].text.strip().replace(',', '.')
#                 print(f"  {num}: Код {code}, Баллы {score_str}")
#                 if score_str and (score_str.isdigit() or score_str.replace('.', '').isdigit()):
#                     try:
#                         scores.append(float(score_str))
#                     except ValueError:
#                         pass
#             else:
#                 print(f"  Строка: недостаточно колонок (найдено {len(cols)})")
#
#         # --- Статистика ---
#         if scores:
#             min_score = min(scores)
#             max_score = max(scores)
#             avg_score = sum(scores) / len(scores)
#             print(f"\n📊 Статистика баллов (всего {len(scores)} записей):")
#             print(f"   Минимальный балл: {min_score}")
#             print(f"   Максимальный балл: {max_score}")
#             print(f"   Средний балл: {avg_score:.2f}")
#         else:
#             print("⚠️ Баллы не найдены")
#
#     except Exception as e:
#         print(f"❌ Ошибка: {e}")
#         traceback.print_exc()
#     finally:
#         driver.quit()
#         print("\n✅ Парсинг завершён.")
#
# if __name__ == '__main__':
#     parse_spbu()

def parse_spbu_program(program_obj):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(program_obj.url)
        wait = WebDriverWait(driver, 20)
        header = wait.until(EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Сумма конкурсных баллов')]")))
        table = header.find_element(By.XPATH, "./ancestor::table")
        rows = table.find_elements(By.TAG_NAME, 'tr')
        if len(rows) < 2:
            return


        scores = []
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 3:
                score_str = cols[2].text.strip().replace(',', '.')
                try:
                    scores.append(float(score_str))
                except ValueError:
                    pass

        if not scores:
            return


        scores.sort(reverse=True)

        budget = program_obj.budget_places or 0
        if budget > 0:
            passed_scores = scores[:budget]
            if passed_scores:
                min_passed = min(passed_scores)
                avg_passed = sum(passed_scores) / len(passed_scores)
                program_obj.min_score_passed = min_passed
                program_obj.avg_score_passed = round(avg_passed, 2)
            else:
                program_obj.min_score_passed = None
                program_obj.avg_score_passed = None
        else:
            program_obj.min_score_passed = None
            program_obj.avg_score_passed = None

        program_obj.save()


    finally:
        driver.quit()

from .models import Program

def update_all_programs():

    programs = Program.objects.all()
    for program in programs:
        parse_spbu_program(program)




















