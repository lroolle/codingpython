import requests


def main():
    n = 100
    url = "https://baidu.com"
    print(f"Making {n} request with requests.")
    session = requests.Session()
    for i in range(n):
        resp = session.get(url)
        if resp.status_code == 200:
            pass


if __name__ == "__main__":
    main()
