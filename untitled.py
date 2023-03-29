


def funA(fn):
    print("testA start")
    fn()
    print("TestA end!")
    # return 0

@funA
def funB():
    """ProxyPool cli工具"""
    print("testB start")
    print("TestB end！")

if __name__ == '__main__':
    # funA(fn)

    print('\n')

    funB()