import json


class FlowerTrans:
    def __init__(self):
        self.dict = {}
        self.loadDict()

    def loadDict(self):
        with open("app/core/flowerTrans.json", "r", encoding="utf-8") as f:
            self.dict = json.load(f)

    def trans(self, text):
        print("translate text for flower: ", text)
        if text in self.dict:
            result = self.dict[text]
        else:
            result = text
        print("result: ", result)
        return result
