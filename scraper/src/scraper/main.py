""""
Clicking the next badge as opposed to using the URL to navigate to the next page
caused 'query_selector' to not detect all items on the page past page 2.
"""

import nodriver as nd
import random
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions
import os


# Accept cookies; possibly aids remaining undetected
def init_db():
    # Load environment variables from .env
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            schema="public",
        ))


async def main():
    supabase: Client = init_db()
    # Initiate nodriver
    browser = await nd.start(headless = False, user_data_dir = "./profile")
    tab = await browser.get('https://jellycat.com/shop-all#/sort:ss_days_since_created:asc')
    await tab.sleep(3)

    cookies = await (tab.query_selector("#onetrust-accept-btn-handler"))
    if cookies:
        await cookies.click()
    popup = await tab.query_selector(".go3588653706")
    if popup:
        await popup.click()
    await browser.cookies.save()
    await tab.sleep(3)
    await tab.get_content()
    current_page = 1

    # Calculate number of pages based on total number of items; assumes 3x12 grid
    total_products_str = await tab.query_selector(".tw-mr-8")
    total_products_float = float(total_products_str.text) if total_products_str else 0
    total_pages = round(total_products_float / 36)
    # Loop through all pages
    for i in range(total_pages):
        jellies = await tab.select_all(".product")
        #print("PAGE " + str(current_page) + "ITEMS " + str(len(jellies)))
        for jelly in jellies:
            # Commit new jelly to database or update availability
            try:

                card = await jelly.query_selector(".card-figure__link")
                #Strips price from jellies name
                name = card.attrs["aria-label"].replace("'", "").split(",", 1)[0]
                url = card.attrs["href"]
                badge = await jelly.query_selector(".ss__badge")
                availability = badge.text if badge else "Available"
                button_disabled = await jelly.query_selector(".disabled")
                stock = False if button_disabled else True
                print("NAME: " + name + " URL: " + url + " STOCK: " + str(stock) + " AVAILABILITY: " + availability)
                supabase.table("jellies").upsert(
                    {"name": name, "url": url, "stock": stock, "availability": availability},
                    on_conflict="name",
                ).execute()
            except:
                print("                                                         ERROR")

        # Delay loading next page
        await tab.sleep(random.randint(2, 7))
        if random.randint(0, 1) == 1:
            await tab.sleep(random.randint(1, 4))
        current_page += 1
        tab = await browser.get("https://jellycat.com/shop-all?page=" + str(current_page) + "#/sort:ss_days_since_created:asc")
        await browser.cookies.load()
        await tab.sleep(3)
        await tab.get_content()
    await tab.close()

if __name__ == "__main__":
    nd.loop().run_until_complete(main())
