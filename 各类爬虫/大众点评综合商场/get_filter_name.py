import sqlite3


def get_shop_name():
    db = sqlite3.connect('shop_data.db')
    cursor = db.cursor()
    sql = 'select distinct shop_type from shop_name'
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    db.close()
    filter_list = []
    for data in datas:
        filter_list.append(int(data[0]))
    return filter_list


def create_db():
    db = sqlite3.connect('shop_data.db')
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS shop_name(
            shop_id integer PRIMARY KEY AUTOINCREMENT,
            shop_name varchar(255) default NULL,
            shop_type varchar(255) default NULL);"""
    cursor.execute(sql)
    cursor.close()
    db.close()


# def test_get_filter_name():
#     list1 = [i for i in range(1, 26)]
#     print(list1)
#     list2 = [list1[i:i + 5] for i in range(0, len(list1), 5)]
#     print(list2)
#     filter_list = get_shop_name()
#     print(filter_list)
#     list3 = []
#     for li_list in list2:
#         li_list2 = li_list[::-1]
#         for shop_name in li_list2:
#             if shop_name in filter_list:
#                 index2 = li_list.index(shop_name)
#                 print(index2)
#                 li_list = li_list[index2:]
#                 print(li_list)
#                 break
#         list3.append(li_list)
#     print(list3)


def test_get_filter_name(list_url, list_name):
    print(list_url)
    print(list_name)
    filter_list = get_shop_name()
    print(filter_list)
    print(list_url)
    print(list_name)
    list3 = []
    for index, li_list in enumerate(list_name):
        li_list2 = li_list[::-1]
        index2 = 0
        for shop_name in li_list2:
            if shop_name in filter_list:
                index2 = li_list.index(shop_name)
                break
        if index2:
            li_list = list_url[index][index2:]
        else:
            li_list = list_url[index]
        print(li_list)
        list3.append(li_list)
    print(list3)


if __name__ == '__main__':
    # get_shop_name()
    list1 = [i for i in range(1, 26)]
    list2 = [list1[i:i + 5] for i in range(0, len(list1), 5)]
    list3 = [i for i in range(51, 76)]
    list4 = [list3[i:i + 5] for i in range(0, len(list3), 5)]
    test_get_filter_name(list2, list4)
    # test_get_filter_name()
    # create_db()