import requests
import os


class DownLoader:

    def __init__(self, socks5='socks5.txt'):

        self.session = requests.Session()
        if os.path.isfile(socks5):
            self.__add_socks5(socks5)

        header_setting = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
        self.session.headers.update(header_setting)

    def __add_socks5(self, socks5):

        with open(socks5, 'r') as f:
            socks5 = f.readline().strip()
            new_ip_address = f.readline().strip()

        self.session.proxies = {'http': socks5, 'https': socks5}

        # get the new ip address
        new_ip = self.session.get('http://httpbin.org/ip').json()

        assert new_ip['origin'] == new_ip_address, "The new ip is not the same as the one in the"
        print("Match! The new ip is " + new_ip_address)

    def down_files(self, urls, write_content=False):
        for url in urls:
            content = self.session.get(url[1])
            if write_content:
                with open(url[0], 'wb') as f:
                    f.write(content.content)
            return content.content

