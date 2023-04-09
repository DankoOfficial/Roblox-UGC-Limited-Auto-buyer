from requests import get, Session
from uuid import uuid4
from threading import Thread

class S:
    userID = 0
    csrf = 0

def csrf():
    return session.post('https://auth.roblox.com/v2/login').headers['x-csrf-token']

def info():
    global product_id, price, creator, collid
    collid = get(f'https://catalog.roblox.com/v1/catalog/items/{id}/details?itemType=Asset').text.split("'collectibleItemId': '")[1].split("'")[0]
    data = session.post('https://apis.roblox.com/marketplace-items/v1/items/details',json = {"itemIds": collid}, headers = {'x-csrf-token': csrf()}).json()[0]
    product_id = data['collectibleProductId']
    price = data['price']
    creator = data['creatorId']

def check():
    info = session.post("https://catalog.roblox.com/v1/catalog/items/details",json={"items": [{"itemType": "Asset", "id": id}]},headers={"x-csrf-token": S.csrf}, cookies={".ROBLOSECURITY": cookie}).json()
    return int([info['unitsAvailableForConsumption'],info['priceStatus']])

def autobuy():
    response = session.post(f'https://apis.roblox.com/marketplace-sales/v1/item/{collid}/purchase-item',json = {"collectibleItemId": collid,"expectedCurrency": 1,"expectedPrice": price,"expectedPurchaserId": str(creator),"expectedPurchaserType": "User","expectedSellerId": 1,"expectedSellerType": "User","idempotencyKey": str(uuid4()),"collectibleProductId": product_id},headers = {'X-CSRF-TOKEN': S.csrf})
    if not response.json()["purchased"]:
        print(f"Failed to buy the limited - {product_id}")
        c = check()
        if c[0] == 0:
            print(">> [LOGS] - ERROR: NO MORE UNITS LEFT")
        elif c[1] == "Off Sale":
            print(">> [LOGS] - ERROR: ITEM IS OFF-SALE")
        else:
            print(f">> [LOGS] - ERROR: UNKNOWN ERROR - {response.text}")
    else:
        print(f">> [LOGS] - BOUGHT ITEM SUCCESSFULLY")

cookie = input('>> Cookie: ')
id = input(">> Assest ID: ")
threads = input(">> Threads (Amount to buy/second): ")
session = Session()
session.cookies['.ROBLOSECURITY'] = cookie
S.userID = session.get('https://www.roblox.com/my/settings/json', cookies={".ROBLOSECURITY": cookie}).json()['UserId']
print(S.userID)
S.csrf = csrf()
print(f">> [LOGS] - GOT CSRF: {S.csrf}")
print(f">> [LOGS] - GETTING MORE INFO ON ITEM")
info()
print(f">> [LOGS] - Product ID: {product_id} - Price: {price} - Creator ID: {creator} - Collectible ID: {collid}")

threads = []
for _ in range(int(threads)):
    t = Thread(target=autobuy)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
