"""
All credits go to lzlis, who makes parsing Aigis data possible.
http://millenniumwaraigis.wikia.com/wiki/User_blog:Lzlis/Downloading_and_Interpreting_Game_Files

Usage: To get next week's "CallServant"
1. Start the game as usual until see the begin screen, then right click to open inspection in browser.
2. Go to network tab to monitor incoming files.
3. Left click on the game screen to start loading game files into browser.
4. In the first few files, find "1fp32igvpoxnb521p9dqypak5cal0xv0" file under the network tab. You should be able to
find the link in that file. Copy it to the browser address and download it.
5. Start this program. It will parse the link to the image and use request library to download it.
    If you want to use socks5 during connection, write the following in 'socks5.txt' under the same folder:
            socks5://username:password@socksurl:port(1080,or 80, etc)
            38.132.115.192 (proxy ip address to verify connection setup)
    The download_files.py will check the ip address. If it doesn't match with the socks5' ip, it will stop for safety.
"""
import download_files
from PIL import Image


def parse_link_file(file_name, key=0xea ^ 0x30, write_list=False):
    """
    x^y is bitwise exclusive or
    :param file_name: file downloaded from browser, containing all links to sources
    :param key: pre-specified for decoding
    :return: nested list of all links
            [[file name, url], ...]
    """

    def clean_mess_links(link):
        aigis_base_url = "http://assets.millennium-war.net"
        parts = link.split(',')
        url = "/".join([aigis_base_url, parts[0], parts[1]])
        name = parts[-1]
        return [name, url]

    with open(file_name, 'rb') as f:
        links = f.readlines()[0]

    links = [chr(link ^ key) for link in links]  # convert all bytes into char
    links = ''.join(links).strip()  # get one long list and erase empty space

    links = links.split('\n')  # split links
    links = [clean_mess_links(link) for link in links]  # [[file name, url],[,] ...]

    if write_list:
        with open('list of urls.txt', 'w') as f:
            links_out = [' : '.join(url) for url in links]
            f.writelines('\n'.join(links_out))

    return links


def get_raw_img_size(raw_img_bytes):
    # Thanks to lzlis's script

    img_info = raw_img_bytes[:1200]
    img_info_chr = [chr(x) for x in img_info]
    img_info_chr = "".join(img_info_chr)
    index = img_info_chr.index('RGBA')  # index right on "R"
    offset = index + 8  # skip 'RGBA" and the next 4 bytes
    img_width = int(img_info[offset]) + int(img_info[offset + 1]) * 256
    offset += 4
    img_high = int(img_info[offset]) + int(img_info[offset + 1]) * 256
    return (img_width, img_high)


if __name__ == '__main__':
    file = "1fp32igvpoxnb521p9dqypak5cal0xv0"
    downloader = download_files.DownLoader()
    urls = parse_link_file(file, write_list=False)

    file_to_download = "MenuCallServant.atx"
    files = [url for url in urls if url[0].endswith(file_to_download)]

    raw_img = downloader.down_files(files, write_content=False)

    img = Image.frombytes('RGBA', get_raw_img_size(raw_img), raw_img, "raw")
    img.save(file_to_download + '.png')
