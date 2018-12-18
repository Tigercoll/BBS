import json
import base64
import urllib.parse
import requests

import qrcode

def base64_encode(base64_str):
    return base64.urlsafe_b64encode((bytes(base64_str,encoding='utf-8'))).decode('utf-8').replace('=', '')


def get_uri(server):
    password = base64_encode(server['password'])
    remarks = server['server'] +' SSR'
    group = 'Tigercoll'
    remarks=base64_encode(remarks)
    group = base64_encode(group)
    obfsparam=''
    try:
        ssr_url = '%s:%s:%s:%s:%s:%s'%(server['server'],
               server['server_port'],
               server['ssr_protocol'],
               server['method'],
               server['obfs'],
               password)

    except Exception as e:
        print('%s'%e)

        ssr_url = '%s:%s:%s:%s:%s:%s' % (server['server'],
                                         server['server_port'],
                                         'origin',
                                         server['method'],
                                         'plain',
                                         password)
    url_back = '/?obfsparam=%s&remarks=%s&group=%s'%(obfsparam,remarks,group)
    full_ulr = ssr_url+url_back
    uri = 'ssr://'+base64_encode(full_ulr)
    print(uri)
    return uri


def main():
    response = requests.get('http://mw-ssr.herokuapp.com/full/json')
    server = response.json()
    uri = get_uri(server)
    img_file = r'py_qrcode.png'
    img = qrcode.make(uri)
    # 图片数据保存至本地文件
    img.save(img_file)
    # 显示二维码图片
    img.show()


if __name__ == '__main__':
    main()