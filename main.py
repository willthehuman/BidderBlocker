from http import client


def main():
    conn = client.HTTPConnection('www.google.com')
    conn.request('GET', '/')
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    print(data)


if __name__ == '__main__':
    main()
