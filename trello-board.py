#!/usr/bin/env python
# coding: utf-8

__doc__ = """
script dùng API tạo 1 Trello board với 2 list "Thứ 3", "Thứ 5",
và tạo 12 card ứng với 12 buổi học của lớp, có set due date ứng với các ngày
học.

Ví dụ kết quả: https://trello.com/b/yEskTV8S/h%E1%BB%8Dc-
python-h%C3%A0-n%E1%BB%99i-pymivn-hn2006-timetable

API: https://developer.atlassian.com/
cloud/trello/guides/rest-api/api-introduction/

https://developer.atlassian.com/cloud/trello/rest/#api-boards-post
https://developer.atlassian.com/cloud/trello/rest/#api-lists-post
https://developer.atlassian.com/cloud/trello/rest/#api-cards-post
"""

import requests
import json
import datetime
import log
from typing import List

logger = log.get_logger(__name__)

key = "_" #Key of Trello, I will upload on Github
token = """_"""

start_date = datetime.datetime(2023, 2, 21, 19)
list_day = [3, 5]
url_board = "https://api.trello.com/1/boards/"
url_list = "https://api.trello.com/1/lists"
url_cad = "https://api.trello.com/1/cards"


def create_trello_board(url, name_board, key, token) -> str:
    """
    Create trello board with name

    Input: url, name_board, key, token
    Output: result = "{board_id}"

    :param url, name_board, key, token: str
    :rtype str:
    """
    query = {"name": name_board, "key": key, "token": token}
    response = requests.request("POST", url, params=query)
    return json.loads(response.text)["id"]


def create_trello_list(url, board_id, key, token, list_day) -> List[str]:
    """
    Create trello list in board with id

    Input: url, list_id, name, day, key, token
    Output: result = [id1, id2, id3, ...]

    :param url, board_id, key, token: str
    :param list_day: list
    :rtype list:
    """
    result: List[str] = []
    for day in list_day:
        query = {"name": f"Thứ {day}",
                 "idBoard": board_id,
                 "key": key,
                 "token": token}
        response = requests.request("POST", url, params=query)

        result.append(json.loads(response.text)["id"])
    return result


def create_trello_cad(url, list_id, name, day, key, token) -> dict:
    """
    Create trello cad in list with id

    Input: url, list_id, name, day, key, token
    Output: result = {}

    :param url, list_id, name, day, key, token: str
    :rtype dict:
    """
    headers = {"Accept": "application/json"}
    query = {"idList": list_id,
             "name": name,
             "due": day,
             "key": key,
             "token": token}
    response = requests.request("POST", url, headers=headers, params=query)
    return json.loads(response.text)


def create_schedule(start_date: datetime) -> List[tuple]:
    """
    Create list schedule with start date

    Input: date
    Output: result = [(1, "dd-mm-yyyy"), ...]

    :param start_date: str
    :rtype dict:
    """
    result: List[tuple] = []
    for i in range(1, 13):
        if i == 1:
            result.append((i, str(start_date)))
            start_date += datetime.timedelta(days=2)
        elif i % 2 == 0:
            result.append((i, str(start_date)))
            start_date += datetime.timedelta(days=5)
        else:
            result.append((i, str(start_date)))
            start_date += datetime.timedelta(days=2)
    return result


def create_trello_board_with_cad(key, token) -> str:
    """
    Create Board with List of Cad by Trello Board API

    Input: key, token of user
    Output: result = ["_value", "shortlink"]

    :param key, token: str
    :rtype dict:
    """
    schedule = create_schedule(start_date)
    board_id = create_trello_board(
        url_board, "PYMI 2302 By Trello Board API", key, token
    )
    list_id = create_trello_list(url_list, board_id, key, token, list_day)

    for name, day in schedule:
        if name % 2 == 0:
            create_trello_cad(url_cad, list_id[1],
                              f"Bài {name}", day, key, token)
        else:
            create_trello_cad(url_cad, list_id[0],
                              f"Bài {name}", day, key, token)

    # Result: https://trello.com/b/kJa9K3gA/pymi-2302by-trello-board-api

    url = f"https://api.trello.com/1/boards/{board_id}/shortLink"

    query = {"key": key, "token": token}

    response = requests.request("GET", url, params=query)

    return json.loads(response.text)


def solve(key, token):
    """Function `solve` dùng để `test`

    :param key, token: number
    :rtype dict:
    """

    logger.debug(f"""Create Board with List of Cad by Trello Board API""")
    result = create_trello_board_with_cad(key, token)
    return result


def main():
    short_link = solve(key, token)
    print(f"https://trello.com/b/{short_link['_value']}")


if __name__ == "__main__":
    main()
