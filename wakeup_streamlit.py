import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright

URLS = [
    'https://lectures-wj5j9nqp2c7ctbuxhvmfsn.streamlit.app/',
    'https://lecturesgit-7qf8cfkcudhcqy97pf4afc.streamlit.app/',
    'https://lectures-tqnrpqrvdfn5qpatskut5h.streamlit.app/',
    'https://lectures-v7ldtzhfzqb6xqt5afofja.streamlit.app/',
    'https://lectures-br8rkbmbqctfhyyj4zckv8.streamlit.app/',
    'https://lectures-4osr5rfiacgjiz3gk48nuv.streamlit.app/',
    'https://lectures-pvwvzsjsth9uhrmcp5vgne.streamlit.app/'
]

log_file = Path(__file__).parent / 'wakeup_streamlit.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


async def visit(page, url):
    try:
        await page.goto(url, timeout=30000, wait_until='domcontentloaded')
        await page.wait_for_timeout(3000)

        # スリープ中はウェイクアップボタンが表示される
        wake_button = page.locator('button', has_text='Yes, get this app back up!')

        if await wake_button.count() > 0 and await wake_button.first.is_visible():
            await wake_button.first.click()
            log.info(f'[WOKE UP] {url}')
        else:
            log.info(f'[ALIVE]   {url}')
    except Exception as e:
        log.error(f'[ERROR]   {url}: {e}')


async def main():
    async with async_playwright() as p:
        # Raspberry Pi (ARM) ではシステムChromiumを使う
        # sudo apt install chromium-browser
        import shutil
        chromium = shutil.which('chromium-browser') or shutil.which('chromium')
        launch_args = {'headless': True, 'executable_path': chromium} if chromium else {'headless': True}
        browser = await p.chromium.launch(**launch_args)
        page = await browser.new_page()
        for url in URLS:
            await visit(page, url)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
