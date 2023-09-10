import random
import requests
from bs4 import BeautifulSoup


# def get_lottory():
#     nums = sorted(random.sample(list(range(1, 50)), 6))
#     spec_numbers = random.randint(1, 50)
#     nums = ",".join(map(str, nums)) + f" 特別號:{spec_numbers}"
#     print(nums)
#     return nums


def get_big_lottory():
    url = "https://www.taiwanlottery.com.tw/lotto/lotto649/history.aspx"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        trs = soup.find("table", class_="table_org td_hm").find_all("tr")
        nums = trs[4].text.split()[1:]
        big_lottory = ",".join(nums[:-1]) + f" 特別號:{nums[-1]}"
        date = ",".join(trs[1].text.split()[:2])
        result = f"期別數/日期: {date}\n號碼: {big_lottory}"
        print(result)

        return result
    except Exception as e:
        print(e)
    return "查詢失敗! 請稍後查詢..."


# if __name__ == "__main":
#     get_big_lottory()
get_big_lottory()
