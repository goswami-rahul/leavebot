from pyppeteer.page import Page
from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pyppeteer.element_handle import ElementHandle
import asyncio


HEADLESS = False

async def login(userid, passwd, page: Page):
    login_url = 'https://llama.greythr.com/uas/portal/auth/login'
    await page.goto(login_url)
    await page.waitFor(3000)
    userid_selector = 'app-login > section > div > div > div > div:nth-child(1) > gt-icon-input > div > input'
    passwd_selector = 'app-login > section > div > div > div > div:nth-child(2) > gt-icon-input > div > input'
    login_selector = 'app-login > section > div > div > div > div:nth-child(3) > button > h6'
    
    element: ElementHandle = await page.J(userid_selector)
    await element.focus()
    await page.keyboard.type(userid)

    element: ElementHandle = await page.J(passwd_selector)
    await element.focus()
    await page.keyboard.type(passwd)

    element: ElementHandle = await page.J(login_selector)
    await element.click()
    await page.waitForSelector('#feeds')


async def apply_leave(page: Page, leave_options=None):
    leave_options = leave_options if leave_options else {}
    leave_url = 'https://llama.greythr.com/v2/employee/apply?key=/v2/employee/apply/leave'
    await page.goto(leave_url)
    await page.waitForNavigation()
    
    # cookies for leave page
    cookies = await page.cookies()
    
    await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > i')
    element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
    await element.click()

    await page.waitForSelector('body > ul:nth-child(19) > li:nth-child(1) > a')
    element: ElementHandle = await page.J('body > ul:nth-child(19) > li:nth-child(1) > a')
    await element.click()
    
    element: ElementHandle = await page.J('body > ul:nth-child(19) > li > a')
    await element.click()
    
    # await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
    # element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(1) > div.span4 > div > div > div > input.cb-autocomplete.ui-autocomplete-input')
    # await element.focus()
    # await page.keyboard.type(leave_options.get('leave_type', 'Paid-Sick-Casual'))
    # element: ElementHandle = await page.J('body > ul:nth-child(19) > li > a')
    # await element.click()

    await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(2) > div.span4 > div > div > input')
    element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(2) > div.span4 > div > div > input')
    await element.focus()
    await page.keyboard.type(leave_options.get('from_date', '11 Dec 2019'))

    await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(3) > div.span4 > div > div > input')
    element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(3) > div.span4 > div > div > input')
    await element.focus()
    await page.keyboard.type(leave_options.get('to_date', '13 Dec 2019'))

    await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(6) > div > div > div > div > input.cb-autocomplete.input-xlarge.ui-autocomplete-input')
    element: ElementHandle = await page.J('#gts-employee-apply-leave > form > fieldset > div:nth-child(6) > div > div > div > div > input.cb-autocomplete.input-xlarge.ui-autocomplete-input')
    await element.focus()
    await page.keyboard.type(leave_options.get('apply_to', 'Prince Chauhan (S12609)'))

    if 'reason' in leave_options:
        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div.row.manualReason > div > div > div > textarea')
        element: ElementHandle = await page.get('#gts-employee-apply-leave > form > fieldset > div.row.manualReason > div > div > div > textarea')
        await element.focus()
        await page.keyboard.type(leave_options['reason'])

    if 'contact_details' in leave_options:
        await page.waitForSelector('#gts-employee-apply-leave > form > fieldset > div:nth-child(8) > div > div > div > textarea')
        element: ElementHandle = await page.get('#gts-employee-apply-leave > form > fieldset > div:nth-child(8) > div > div > div > textarea')
        await element.focus()
        await page.keyboard.type(leave_options['contact_details'])

    # submit: ElementHandle = await page.J('#gts-employee-apply-leave > form > div > button.btn.btn-primary')
    # await submit.click()

async def go(userid, passwd):
    browser: Browser = await launch(headless=HEADLESS)
    try:
        page, = await browser.pages()
        await login(userid, passwd, page)
        await apply_leave(page)
    finally:
        await browser.close()

userid, passwd = 'T12546', '@123456789'
asyncio.run(go(userid, passwd))