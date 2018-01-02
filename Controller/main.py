from Controller.controller import subscribe, main, key_mapping

def myMethod(test: int, test2:int):
    print(key_mapping[test])

subscribe(myMethod)
main()
