import sys

from telethon import TelegramClient

if __name__ == '__main__':
    phone = sys.argv[1]
    password = sys.argv[2]
    api_id = sys.argv[3]
    api_hash = sys.argv[4]
    useProxy = sys.argv[5] if len(sys.argv) > 5 else None

    proxy = None
    if useProxy is not None and useProxy != "false":
        print("useProxy is " + useProxy)
        host = "127.0.0.1"
        port = 1080
        proxy = ("socks5", host, port)

    print(proxy)
    client = TelegramClient(phone, api_id, api_hash, proxy=proxy).start(phone=phone, password=password)

    channel_username = 'kxswa'


    async def dow():
        dialog = await client.get_entity(channel_username)
        async for msg in client.iter_messages(dialog, limit=1):
            with open("订阅链接.txt", "w", encoding="utf8") as f:
                f.write(msg.message)


    client.loop.run_until_complete(dow())
