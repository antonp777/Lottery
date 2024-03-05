import math


def generate_data_for_report(list_data, item_in_page):
    count_page = math.ceil(len(list_data) / item_in_page)

    num_page = range(1, count_page + 1)

    cont_page = []
    for x in range(0, len(list_data), item_in_page):
        cont_page.append(list_data[x:x + item_in_page])

    result_dict = dict(zip(num_page, cont_page))

    return result_dict
