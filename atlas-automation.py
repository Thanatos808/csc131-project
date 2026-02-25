import re, time
from datetime import datetime
from click import option
from playwright.sync_api import Playwright, sync_playwright, expect
# CONFIG
USERNAME = "Sacstatecpr@outlook.com"
PASSWORD = "ssCPR123*"  
INSTRUCTOR_NAME = "sac"  
DATE = "02/19/2026"  

# TO DO !!!!
# ACTION --> VIEW
# ACCEPT THE STUDENT (TWICE)
# READ THE STUDENT'S INFO
def select_date(page, date_str):
    target_date = datetime.strptime(DATE, "%m/%d/%Y")
    target_month_year = target_date.strftime("%B %Y")   # February 2026
    target_day = str(target_date.day)                   # 19

    # Open date picker
    page.get_by_role("button", name=re.compile("Choose a Date Range")).click()

    # Wait for calendar to appear
    page.wait_for_selector(".react-calendar")

    # Navigate to correct month
    while True:
        visible_month = page.locator(".react-calendar__navigation__label").inner_text()

        if target_month_year in visible_month:
            break

        page.get_by_role("button", name=re.compile("Next")).click()

    # Click the correct day
    page.get_by_role("button", name=target_day).click()

    
def run(playwright: Playwright) -> None:
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
    page.get_by_role("textbox", name="Instructor").click()
    page.get_by_role("textbox", name="Instructor").fill(INSTRUCTOR_NAME)
    page.wait_for_timeout(500)
    page.get_by_role("listitem").filter(has_text="/ Sac State").click()
    
    

    # SELECT DATE
    select_date(page, DATE)
    time.sleep(60)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
# playwright codegen https://atlas.heart.org