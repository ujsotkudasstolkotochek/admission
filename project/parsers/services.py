# services.py
from .models import Program, Applicant
import re
import os
import time
import subprocess
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# ------------------------------------------------------------
# Вспомогательные функции
# ------------------------------------------------------------

def retry_on_connection_error(driver, url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            driver.get(url)
            return
        except (WebDriverException, ConnectionResetError, TimeoutException) as e:
            print(f"⚠️ Попытка {attempt+1}/{retries} не удалась: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(delay)

def kill_chromedrivers():
    try:
        subprocess.run(
            ['wmic', 'process', 'where',
             "name='chrome.exe' and commandline like '%--headless%'",
             'delete'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        subprocess.run(
            ['taskkill', '/f', '/im', 'chromedriver.exe'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
    except Exception:
        pass
def sync_applicants(program_obj, applicants_data):
    """Полностью пересоздаёт записи для программы (удаляет старые, создаёт новые)."""
    if not applicants_data:
        deleted = Applicant.objects.filter(program=program_obj).delete()[0]
        return {'created': 0, 'updated': 0, 'deleted': deleted}

    deleted = Applicant.objects.filter(program=program_obj).delete()[0]
    created = 0
    for data in applicants_data:
        position = data.get('position')
        Applicant.objects.create(
            program=program_obj,
            position=position,
            code=data['code'],
            score=data['score'],
            status=data['status'],
        )
        created += 1
    return {'created': created, 'updated': 0, 'deleted': deleted}


# ------------------------------------------------------------
# Парсер для СПбГУ (исправлена статистика)
# ------------------------------------------------------------

def parse_spbu_program(program_obj):
    kill_chromedrivers()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print(f"⏳ Парсинг СПбГУ: {program_obj.code} {program_obj.name}")
        retry_on_connection_error(driver, program_obj.url)
        time.sleep(5)

        wait = WebDriverWait(driver, 30)

        header = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//th[contains(text(), 'Сумма конкурсных баллов')]")
        ))
        table = header.find_element(By.XPATH, "./ancestor::table")
        wait.until(EC.presence_of_element_located((By.XPATH, ".//tr[position()>1]")))
        rows = table.find_elements(By.TAG_NAME, 'tr')
        if len(rows) < 2:
            print("⚠️ Таблица пуста")
            return

        common_scores = []
        applicants_data = []
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 3:
                position = int(cols[0].text.strip())
                code = cols[1].text.strip()
                score_str = cols[2].text.strip().replace(',', '.')
                try:
                    score = float(score_str)
                except ValueError:
                    score = 0.0

                status_text = ''
                if len(cols) > 6:
                    status_text = cols[6].text.strip()

                if 'Целевое' in status_text:
                    status = 'target'
                elif 'Особая квота' in status_text:
                    status = 'special'
                elif 'Без вступительных' in status_text:
                    status = 'no_exam'
                elif 'Участвует в конкурсе' in status_text:
                    status = 'common'
                else:
                    status = 'common'

                applicants_data.append({
                    'position': position,
                    'code': code,
                    'score': score,
                    'status': status,
                })
                if status == 'common' and score > 0:
                    common_scores.append(score)

        if not applicants_data:
            print("⚠️ Данные не найдены")
            return

        stats = sync_applicants(program_obj, applicants_data)

        common_scores.sort(reverse=True)
        budget = program_obj.budget_places or 0
        if budget > 0 and common_scores:
            passed_scores = common_scores[:budget]
            if passed_scores:
                program_obj.min_score_passed = min(passed_scores)
                program_obj.avg_score_passed = round(sum(passed_scores) / len(passed_scores), 2)
            else:
                program_obj.min_score_passed = None
                program_obj.avg_score_passed = None
        else:
            program_obj.min_score_passed = None
            program_obj.avg_score_passed = None
        program_obj.save()

        print(f"✅ Обновлена программа {program_obj.code}: создано {stats['created']}, обновлено {stats['updated']}, удалено {stats['deleted']}")

    except Exception as e:
        print(f"❌ Ошибка при парсинге СПбГУ: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
        try:
            user_data_dir = driver.capabilities['chrome']['userDataDir']
            if user_data_dir and os.path.exists(user_data_dir):
                import shutil
                shutil.rmtree(user_data_dir, ignore_errors=True)
                print("🧹 Временный профиль Chrome удалён")
        except Exception as e:
            print(f"⚠️ Не удалось удалить временный профиль: {e}")
        kill_chromedrivers()


# ------------------------------------------------------------
# Парсер для СПбПУ (исправлена статистика, добавлена "Отдельная квота")
# ------------------------------------------------------------

def parse_spbpu_program(program_obj):
    kill_chromedrivers()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print(f"⏳ Парсинг СПбПУ: {program_obj.code} {program_obj.name}")
        retry_on_connection_error(driver, "https://my.spbstu.ru/home/abit/list-applicants/bachelor")
        time.sleep(5)

        wait = WebDriverWait(driver, 30)

        form = wait.until(EC.presence_of_element_located((By.ID, "educationOfForm")))
        Select(form).select_by_visible_text("Очная")
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", form)
        time.sleep(2)

        cond = wait.until(EC.presence_of_element_located((By.ID, "conditions")))
        Select(cond).select_by_visible_text("Бюджетная основа")
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", cond)
        time.sleep(2)

        code_select = wait.until(EC.presence_of_element_located((By.ID, "code")))
        found = False
        for option in code_select.find_elements(By.TAG_NAME, "option"):
            if program_obj.code in option.text:
                option.click()
                found = True
                print(f"✅ Выбрано направление: {option.text}")
                break
        if not found:
            print(f"⚠️ Направление {program_obj.code} не найдено в списке")
            return

        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", code_select)
        time.sleep(5)

        table = wait.until(EC.presence_of_element_located((By.ID, "ajaxTable")))
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ajaxTable tbody tr")))
        except TimeoutException:
            time.sleep(5)
            if not table.find_elements(By.CSS_SELECTOR, "tbody tr"):
                print("⚠️ Таблица пуста, возможно, направление не активно")
                return

        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"📋 Найдено строк: {len(rows)}")

        if not rows:
            print("⚠️ Таблица пуста")
            return

        common_scores = []
        applicants_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                try:
                    position = int(cols[0].text.strip())
                except ValueError:
                    position = None
                code_applicant = cols[1].text.strip()
                status_text = cols[2].text.strip()
                score_str = cols[3].text.strip().replace(',', '.')
                try:
                    score = float(score_str)
                except ValueError:
                    score = 0.0

                if 'БВИ' in status_text:
                    status = 'no_exam'
                elif 'Целевое' in status_text:
                    status = 'target'
                elif 'Особая квота' in status_text:
                    status = 'special'
                elif 'Отдельная квота' in status_text:   # добавлено
                    status = 'special'
                elif status_text == 'Нет':
                    status = 'common'
                else:
                    status = 'unknown'

                applicants_data.append({
                    'position': position,
                    'code': code_applicant,
                    'score': score,
                    'status': status,
                })
                if status == 'common' and score > 0:
                    common_scores.append(score)

        if not applicants_data:
            print("⚠️ Данные не найдены")
            return

        stats = sync_applicants(program_obj, applicants_data)

        common_scores.sort(reverse=True)
        budget = program_obj.budget_places or 0
        if budget > 0 and common_scores:
            passed_scores = common_scores[:budget]
            if passed_scores:
                program_obj.min_score_passed = min(passed_scores)
                program_obj.avg_score_passed = round(sum(passed_scores) / len(passed_scores), 2)
            else:
                program_obj.min_score_passed = None
                program_obj.avg_score_passed = None
        else:
            program_obj.min_score_passed = None
            program_obj.avg_score_passed = None
        program_obj.save()

        print(f"✅ Обновлена программа {program_obj.code}: создано {stats['created']}, обновлено {stats['updated']}, удалено {stats['deleted']}")

    except Exception as e:
        print(f"❌ Ошибка при парсинге СПбПУ: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
        try:
            user_data_dir = driver.capabilities['chrome']['userDataDir']
            if user_data_dir and os.path.exists(user_data_dir):
                import shutil
                shutil.rmtree(user_data_dir, ignore_errors=True)
                print("🧹 Временный профиль Chrome удалён")
        except Exception as e:
            print(f"⚠️ Не удалось удалить временный профиль: {e}")
        kill_chromedrivers()


# ------------------------------------------------------------
# Парсер для ИТМО (уже использует common_scores, оставляем как есть)
# ------------------------------------------------------------

def parse_itmo_program(program_obj):
    from .models import Applicant
    import re
    kill_chromedrivers()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://abit.itmo.ru/rating/bachelor/budget/{program_obj.code}"
        print(f"⏳ Парсинг ИТМО: {program_obj.code} {program_obj.name}")
        retry_on_connection_error(driver, url)
        time.sleep(5)

        wait = WebDriverWait(driver, 30)

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Балл ВИ+ИД')]")))

        page_text = driver.find_element(By.TAG_NAME, "body").text

        blocks = re.split(r'\n(?=\d+\s+№\d+)', page_text)
        applicants = []

        for block in blocks:
            if not block.strip():
                continue

            pos_match = re.search(r'^(\d+)\s+№\d+', block)
            if not pos_match:
                continue
            position = int(pos_match.group(1))

            code_match = re.search(r'№(\d+)', block)
            code = code_match.group(1) if code_match else ''

            score_match = re.search(r'Балл ВИ\+ИД:\s*(\d+)', block)
            score = float(score_match.group(1)) if score_match else 0.0

            raw_lower = block.lower()
            if 'олимпиада' in raw_lower or 'без вступительных' in raw_lower or 'бви' in raw_lower:
                status = 'no_exam'
            elif 'отдельная квота' in raw_lower or 'особая квота' in raw_lower:
                status = 'special'
            elif 'целевая' in raw_lower:
                status = 'target'
            else:
                status = 'common'

            applicants.append({
                'position': position,
                'code': code,
                'score': score,
                'status': status,
            })

        print(f"📋 Найдено абитуриентов: {len(applicants)}")

        if not applicants:
            print("⚠️ Данные не найдены")
            return

        stats = sync_applicants(program_obj, applicants)

        common_scores = [app['score'] for app in applicants if app['status'] == 'common' and app['score'] > 0]
        if common_scores:
            common_scores.sort(reverse=True)
            budget = program_obj.budget_places or 0
            if budget > 0:
                passed_scores = common_scores[:budget]
                if passed_scores:
                    program_obj.min_score_passed = min(passed_scores)
                    program_obj.avg_score_passed = round(sum(passed_scores) / len(passed_scores), 2)
                else:
                    program_obj.min_score_passed = None
                    program_obj.avg_score_passed = None
            else:
                program_obj.min_score_passed = None
                program_obj.avg_score_passed = None
            program_obj.save()

        print(f"✅ Обновлена программа {program_obj.code}: создано {stats['created']}, обновлено {stats['updated']}, удалено {stats['deleted']}")

    except Exception as e:
        print(f"❌ Ошибка при парсинге ИТМО: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
        try:
            user_data_dir = driver.capabilities['chrome']['userDataDir']
            if user_data_dir and os.path.exists(user_data_dir):
                import shutil
                shutil.rmtree(user_data_dir, ignore_errors=True)
                print("🧹 Временный профиль Chrome удалён")
        except Exception as e:
            print(f"⚠️ Не удалось удалить временный профиль: {e}")
        kill_chromedrivers()


# ------------------------------------------------------------
# Парсер для МИРЭА
# ------------------------------------------------------------

# ------------------------------------------------------------
# Парсер для МИРЭА (улучшенный)
# ------------------------------------------------------------

def parse_mirea_program(program_obj):
    kill_chromedrivers()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print(f"⏳ Парсинг МИРЭА: {program_obj.code} {program_obj.name}")
        retry_on_connection_error(driver, program_obj.url, retries=2, delay=10)
        time.sleep(5)

        wait = WebDriverWait(driver, 60)  # увеличенный таймаут

        # Ждём появления любой таблицы
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        except TimeoutException:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            print(f"⚠️ Таблица не найдена. Текст страницы (первые 500 символов):\n{page_text[:500]}")
            driver.save_screenshot(f"mirea_error_{program_obj.code}.png")
            print(f"📸 Скриншот сохранён как mirea_error_{program_obj.code}.png")
            return

        # Ищем таблицу с данными
        tables = driver.find_elements(By.TAG_NAME, "table")
        target_table = None
        for table in tables:
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            if rows:
                target_table = table
                break
        if not target_table:
            # пробуем найти строки без tbody
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) > 1:
                    target_table = table
                    break
        if not target_table:
            print("⚠️ Не найдена таблица с данными")
            page_text = driver.find_element(By.TAG_NAME, "body").text
            print(f"Текст страницы (первые 500 символов):\n{page_text[:500]}")
            return

        rows = target_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        if not rows:
            rows = target_table.find_elements(By.TAG_NAME, "tr")
            if rows:
                rows = rows[1:]  # пропускаем заголовок

        print(f"📋 Найдено строк: {len(rows)}")

        if not rows:
            print("⚠️ Таблица пуста")
            return

        common_scores = []
        applicants_data = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 9:
                continue

            try:
                position = int(cols[0].text.strip()) if cols[0].text.strip() else None
                code = cols[1].text.strip() if len(cols) > 1 else ''
                # статус согласия (колонка 4)
                has_consent = cols[4].text.strip().lower() == 'да' if len(cols) > 4 else None

                # статус – пока все как common, можно расширить при необходимости
                status = 'common'

                # сумма баллов – обычно в 10-й колонке (индекс 10)
                score_str = cols[10].text.strip().replace(',', '.') if len(cols) > 10 else '0'
                try:
                    score = float(score_str) if score_str else 0.0
                except ValueError:
                    score = 0.0

                applicants_data.append({
                    'position': position,
                    'code': code,
                    'score': score,
                    'status': status,
                })
                if status == 'common' and score > 0:
                    common_scores.append(score)

            except Exception as e:
                print(f"⚠️ Ошибка при парсинге строки: {e}")
                continue

        if not applicants_data:
            print("⚠️ Данные не найдены")
            return

        stats = sync_applicants(program_obj, applicants_data)

        common_scores.sort(reverse=True)
        budget = program_obj.budget_places or 0
        if budget > 0 and common_scores:
            passed_scores = common_scores[:budget]
            if passed_scores:
                program_obj.min_score_passed = min(passed_scores)
                program_obj.avg_score_passed = round(sum(passed_scores) / len(passed_scores), 2)
            else:
                program_obj.min_score_passed = None
                program_obj.avg_score_passed = None
        else:
            program_obj.min_score_passed = None
            program_obj.avg_score_passed = None
        program_obj.save()

        print(f"✅ Обновлена программа {program_obj.code}: создано {stats['created']}, обновлено {stats['updated']}, удалено {stats['deleted']}")

    except Exception as e:
        print(f"❌ Ошибка при парсинге МИРЭА: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
        try:
            user_data_dir = driver.capabilities['chrome']['userDataDir']
            if user_data_dir and os.path.exists(user_data_dir):
                import shutil
                shutil.rmtree(user_data_dir, ignore_errors=True)
                print("🧹 Временный профиль Chrome удалён")
        except Exception as e:
            print(f"⚠️ Не удалось удалить временный профиль: {e}")



# ------------------------------------------------------------
# Обновление всех программ
# ------------------------------------------------------------

def update_all_programs():
    print("🔄 Начинаем обновление данных...")
    programs = Program.objects.all()
    print(f"Найдено программ: {programs.count()}")
    if not programs:
        print("⚠️ Нет программ для обновления.")
        return

    for program in programs:
        print(f"Обработка программы: {program.code} {program.name}")
        try:
            if 'spbstu.ru' in program.url:
                parse_spbpu_program(program)
            elif 'itmo.ru' in program.url:
                parse_itmo_program(program)
            elif 'mirea.ru' in program.url:      # <-- добавьте эту строку
                parse_mirea_program(program)     # <-- и эту
            else:
                parse_spbu_program(program)
        except Exception as e:
            print(f"❌ Ошибка при обработке {program.code}: {e}")
        time.sleep(2)
    print("✅ Обновление завершено.")

# ------------------------------------------------------------
# Тестовые функции (без изменений)
# ------------------------------------------------------------

def test_spbpu():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        print("=" * 80)
        print("Открываем страницу СПбПУ")
        print("=" * 80)

        driver.get("https://my.spbstu.ru/home/abit/list-applicants/bachelor")
        time.sleep(5)

        form = driver.find_element(By.ID, "educationOfForm")
        cond = driver.find_element(By.ID, "conditions")
        code_select = driver.find_element(By.ID, "code")

        Select(form).select_by_visible_text("Очная")
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", form)
        time.sleep(3)

        Select(cond).select_by_visible_text("Бюджетная основа")
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", cond)
        time.sleep(3)

        target_text = "09.03.03 Прикладная информатика"
        found = False
        for option in code_select.find_elements(By.TAG_NAME, "option"):
            if target_text in option.text:
                option.click()
                found = True
                print(f"✅ Выбрано направление: {option.text}")
                break
        if not found:
            print(f"⚠️ Направление '{target_text}' не найдено, выбираем первое доступное")
            options_list = code_select.find_elements(By.TAG_NAME, "option")
            if len(options_list) > 1:
                options_list[1].click()
                print(f"✅ Выбрано направление: {options_list[1].text}")

        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", code_select)
        time.sleep(8)

        table = driver.find_element(By.ID, "ajaxTable")
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        if rows:
            print("\n📋 Первые 10 строк таблицы (№, Код, Основание, Сумма баллов):")
            for i, row in enumerate(rows[:10]):
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    num = cols[0].text.strip()
                    code = cols[1].text.strip()
                    status = cols[2].text.strip()
                    score = cols[3].text.strip()
                    print(f"  {i+1}. №{num} | Код {code} | Основание: {status} | Баллы: {score}")
                else:
                    print(f"  Строка {i+1}: недостаточно колонок ({len(cols)})")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
        print("\n✅ Тест завершён")


def test_itmo(code='2334'):
    """
    Тестовый парсинг рейтинга ИТМО для заданного направления.
    code – ID направления (по умолчанию 2334 для Прикладной математики и информатики)
    """
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    import re

    try:
        import subprocess
        subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=False)
    except:
        pass

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://abit.itmo.ru/rating/bachelor/budget/{code}"
        print(f"⏳ Открываем страницу ИТМО: {url}")
        driver.get(url)

        time.sleep(5)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "404" in body_text or "не найдена" in body_text:
            print("⚠️ Страница не найдена (404). Проверьте код направления.")
            return

        wait = WebDriverWait(driver, 30)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Балл ВИ+ИД')]")))
            print("✅ Найден блок с баллами")
        except:
            print("⚠️ Блок с баллами не найден. Пробуем найти любой элемент с '№'...")
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '№')]")))
                print("✅ Найден элемент с '№'")
            except:
                print("❌ Ни один из ожидаемых элементов не найден. Выводим HTML страницы для анализа.")
                print(driver.page_source[:3000])
                return

        page_text = driver.find_element(By.TAG_NAME, "body").text
        print("\n📋 Первые 500 символов страницы (для понимания структуры):")
        print(page_text[:500])

        lines = page_text.split('\n')
        applicants = []
        current = {}
        in_applicant = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^\d+\s+№\d+', line):
                if current:
                    applicants.append(current)
                current = {'raw': line}
                in_applicant = True
            elif in_applicant:
                current['raw'] += ' ' + line
                if 'Есть согласие:' in line:
                    in_applicant = False
                    applicants.append(current)
                    current = {}

        if current:
            applicants.append(current)

        print(f"\n📋 Найдено абитуриентов: {len(applicants)}")

        if not applicants:
            print("⚠️ Абитуриенты не найдены. Возможно, страница пуста или структура отличается.")
            return

        print("\n📋 Первые 10 записей:")
        for i, app in enumerate(applicants[:10]):
            raw = app.get('raw', '')
            code_match = re.search(r'№(\d+)', raw)
            code = code_match.group(1) if code_match else '—'
            score_match = re.search(r'Балл ВИ\+ИД:\s*(\d+)', raw)
            score = score_match.group(1) if score_match else '—'
            consent_match = re.search(r'Есть согласие:\s*(да|нет)', raw, re.IGNORECASE)
            consent = consent_match.group(1) if consent_match else '—'
            status_match = re.search(r'(Зачислен|Конкурс|Не прошел)', raw)
            status = status_match.group(1) if status_match else '—'

            print(f"  {i+1}. Код: {code}, Баллы: {score}, Согласие: {consent}, Статус: {status}")

        match = re.search(r'Количество мест:\s*(\d+)', page_text)
        if match:
            print(f"\n📊 Количество бюджетных мест: {match.group(1)}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        try:
            print("\n📄 HTML страницы (первые 2000 символов):")
            print(driver.page_source[:2000])
        except:
            pass
    finally:
        driver.quit()
        print("\n✅ Тест завершён")


def test_mirea(comp_id='1862638569831537974', edu_level='2', org_unit_id='14840287700495285107', edu_form_id='1'):
    """
    Быстрый тест парсинга страницы МИРЭА.
    Запускать из Django shell:
        from parsers.services import test_mirea
        test_mirea('1862532990899330358')
    """
    kill_chromedrivers()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--silent")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids={comp_id}&edu_level={edu_level}&org_unit_id={org_unit_id}&edu_form_id={edu_form_id}"
        print(f"⏳ Открываем страницу МИРЭА: {url}")
        driver.get(url)
        time.sleep(5)

        wait = WebDriverWait(driver, 60)

        # Пробуем дождаться таблицы
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            print("✅ Таблица найдена.")
        except TimeoutException:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            print(f"⚠️ Таблица не найдена. Текст страницы (первые 500 символов):\n{page_text[:500]}")
            driver.save_screenshot(f"test_mirea_error_{comp_id}.png")
            print(f"📸 Скриншот сохранён как test_mirea_error_{comp_id}.png")
            return

        # Выводим текст страницы для анализа
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print("\n📋 Первые 1500 символов страницы (для анализа):")
        print(page_text[:1500])
        print("\n" + "="*80 + "\n")

        # Ищем таблицы
        tables = driver.find_elements(By.TAG_NAME, "table")
        if not tables:
            print("⚠️ Таблиц не найдено.")
            return

        print(f"Найдено таблиц: {len(tables)}")
        for idx, table in enumerate(tables):
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            if not rows:
                rows = table.find_elements(By.TAG_NAME, "tr")
            if rows:
                print(f"Таблица #{idx+1}: {len(rows)} строк")
                # Выведем первые 10 строк
                for i, row in enumerate(rows[:10]):
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if cols:
                        data = [col.text.strip() for col in cols]
                        print(f"  Строка {i+1}: {data}")
                break

        # Количество мест
        match = re.search(r'Количество мест:\s*(\d+)', page_text)
        if match:
            print(f"\n📊 Количество бюджетных мест: {match.group(1)}")

        match_total = re.search(r'Всего:\s*(\d+)', page_text)
        if match_total:
            print(f"👥 Всего абитуриентов: {match_total.group(1)}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        traceback.print_exc()
        try:
            print("\n📄 HTML страницы (первые 2000 символов):")
            print(driver.page_source[:2000])
        except:
            pass
    finally:
        driver.quit()
        print("\n✅ Тест завершён")