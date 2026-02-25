import re, time
from playwright.sync_api import Playwright, sync_playwright, expect
# CONFIG
USERNAME = "Sacstatecpr@outlook.com"
PASSWORD = "ssCPR123*"  
INSTRUCTOR_NAME = "sac"  
DATE = "2026-03-03"  

# TO DO !!!!
# SELECT INSTRUCTOR
# SELECT DATE
# ACTION --> VIEW
# ACCEPT THE STUDENT (TWICE)
# READ THE STUDENT'S INFO

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

    # NAVIGATING TO CLASS
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
    
    # SELECT INSTRUCTOR (in progress)
    page.locator(".css-19bb58m").first.click()
    page.locator("#react-select-5-option-2").get_by_text("Sac State").click()



    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
