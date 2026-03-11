import email
import re, time
from datetime import datetime
from unicodedata import name
from click import option
from playwright.sync_api import Playwright, sync_playwright, expect

# CONFIG
USERNAME = "Sacstatecpr@outlook.com"
PASSWORD = "ssCPR123*"

# TO DO !!!!
# need to account for non-BLS courses
# add error handling and retries for each step
# account for phone number
def run(playwright: Playwright, instructor_name: str, date_str: str) -> None:
    
    INSTRUCTOR_NAME = instructor_name
    DATE = date_str
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # LOGGING IN
    page.goto("https://atlas.heart.org")
    page.get_by_test_id("login-logout-button1").click()
    page.get_by_role("textbox", name="Username / Email").fill(USERNAME)
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Sign In").click()

    # NAVIGATING TO CLASS WITHOUT USING MENUS
    page.locator('span.MainMenuNavigation_expandConatiner__M5ExW', has_text='Classes').wait_for(state='visible', timeout=30000)
    page.evaluate("""
        const classesSpan = [...document.querySelectorAll('span.MainMenuNavigation_expandConatiner__M5ExW')]
            .find(el => el.textContent.trim() === 'Classes');
        if (classesSpan) {
            const event = new MouseEvent('mouseover', {bubbles: true, cancelable: true});
            classesSpan.dispatchEvent(event);
        }
    """)

    # CLICK TRAINING SITE CLASSES
    page.evaluate("""
        const btn = document.querySelector('button[title="Training Site Classes"]');
        if (btn) btn.click();
    """)

    # ORGANIZATION SELECTION (only needed for testing)
    page.get_by_label("Organization").click()
    page.get_by_label("Organization").fill("Sac State")

    # Wait for dropdown option and click it
    org_option = page.locator("div[role='option']", has_text="Sac State")
    org_option.wait_for(state="visible")
    org_option.click()

    # SELECT INSTRUCTOR (in progress)
    page.get_by_role("textbox", name="Instructor").fill(INSTRUCTOR_NAME)
    page.wait_for_selector("li.option")
    dropdown = page.locator("li.option")
    dropdown.filter(has_text=INSTRUCTOR_NAME).first.click()

    # SELECT DATE
    # define target date components
    target_date = datetime.strptime(DATE, "%m/%d/%Y")
    target_year = str(target_date.year)
    target_month = target_date.strftime("%B")
    target_day = target_date.day     
    weekday_name = target_date.strftime("%A")
    def day_suffix(day):
        if 11 <= day <= 13:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    day_string = f"{target_day}{day_suffix(target_day)}"
    
    # opening calendar
    page.get_by_role("button", name="Choose a Date Range ").click()
    page.wait_for_selector("div.calendar_year__control")
    # year
    year_dropdown = page.locator("div.calendar_year__control")
    year_dropdown.click()  # open dropdown
    page.wait_for_selector("div[role='listbox']")
    page.locator("div[role='listbox'] div").filter(has_text=target_year).first.click()
    # month
    month_dropdown = page.locator("div.calendar_month__control")
    month_dropdown.click()  # open dropdown
    page.wait_for_selector("div[role='listbox']")
    page.locator("div[role='listbox'] div").filter(has_text=target_month).first.click()
    # day
    day_option_name = f"Choose {weekday_name}, {target_month} {day_string}, {target_year}"
    page.get_by_role("option", name=day_option_name).click()
    page.get_by_role("option", name=day_option_name).click()

    # get the row with the BLS course
    row = page.locator("tr", has_text="BLS Provider Course").first
    row.wait_for(state="visible")  # ensure it's loaded

    # get the discipline span text inside that row
    bls_span_text = row.locator("span.dynamicTable_disciplineStyle__msaHF").text_content() # course
    

    # navigate through action menu to accept the student
    page.get_by_test_id("kebab-items-0").click()
    page.get_by_test_id("action-menus-0-0").click()
    page.get_by_test_id("acceptbutton").click()
    page.get_by_test_id("acceptBtn").click()

    # get email and name
    email_locator = page.locator("div.dynamicTable_rtlBorderRight__A69BQ").first
    email_locator.wait_for(state="visible", timeout=10000)
    email = email_locator.inner_text()
    name_locator = page.locator("div.dynamicTable_name__viewClass__iM8UX").first
    name_locator.wait_for(state="visible", timeout=10000)
    name = name_locator.inner_text()
    

    # time.sleep(60)
    context.close()
    browser.close()
    return {
        "name": name,
        "email": email,
        "discipline": bls_span_text,
        "course_date": date_str,
        "instructor": instructor_name
    }
# if __name__ == "__main__":
#     with sync_playwright() as playwright:
#         result = run(playwright, "Sac", "02/09/2026")
#         print(result)
# playwright codegen https://atlas.heart.org