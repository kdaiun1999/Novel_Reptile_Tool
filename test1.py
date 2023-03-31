sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '？']

# def illegal_char_analysis(title):
#
#
#     print(FileName("\/?" * <> | "))
#
#     return title


# def FileName(STR):
#     for i, j in ("/／", "\\＼", "?？", "|︱", "\"＂", "*＊", "<＜", ">＞"):
#         STR = STR.replace(i, j)
#     return STR
# if __name__ == '__main__':
    # temp = FileName("总督德?卡蓬蒂尔")
    # print(temp)
    # with open(temp + ".txt", "w", encoding="utf-8") as f:
    #     f.write("1111")


if __name__ == '__main__':
    import time

    for i in range(100):
        time.sleep(0.5)
        print('\r' + '▇' * (i // 2) + str(i) + '%', end='')