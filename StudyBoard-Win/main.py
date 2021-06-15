import util
import config
import requests
import time


def main():
    while True:
        try:
            resp = requests.post(url=config.api, json={ "token": config.token }, timeout=10)
            json_obj = resp.json()
            if json_obj.get("error") == "invalid":
                util.print_plus("您的登录已过期，请重新登录！")
            else:
                durations = json_obj["durations"]
                for duration in durations:
                    util.notify_duration(duration)
        except:
            util.print_plus("请检查您的网络连接！")
        time.sleep(5)


if __name__ == '__main__':
    main()
