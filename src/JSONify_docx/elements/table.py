from typing import Dict, Any

from more_itertools import peekable

from JSONify_docx.elements import container, el


class table(container):
    __type__ = "table"

    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs": {}}

    def to_json(self, doc) -> Dict[str, Any]:

        content = []
        for elt in self:
            JSON = elt.to_json(doc)

            content.append(JSON)

        self.mergeHandle(content)

        self.out['content'] = content

        return self.out

    def mergeHandle(self, content):
        # 将表格转换成二维数组进行合并处理
        virtual2dArr = []
        for tblRow in content:
            virtual2dArr.append(tblRow['content'])

        rows = len(virtual2dArr)
        memo = [{} for _ in range(rows)]
        for row in range(rows - 1, -1, -1):
            # 获取当前行的列数
            curInx = 0
            cols = len(virtual2dArr[row])
            removeColCnts = 0
            # 获取合并的行数以及删除占位表格
            for col in range(cols):
                curCell = virtual2dArr[row][col]
                if row == rows - 1:
                    memo[row][curInx] = (0, col) if curCell['attrs']['rowspan'] != "continue" else (1, col)
                else:
                    if curCell['attrs']['rowspan'] == "restart":
                        last = memo[row + 1][curInx]
                        accuRow = last[0]
                        removeCol = last[1]
                        curCell['attrs']['rowspan'] = accuRow + 1
                        memo[row][curInx] = (0, col)
                        if virtual2dArr[row + 1][removeCol - removeColCnts]['attrs']['rowspan'] == "continue":
                            del virtual2dArr[row + 1][removeCol - removeColCnts]
                            removeColCnts += 1
                    elif curCell['attrs']['rowspan'] == "continue":
                        if curInx in memo[row + 1]:
                            last = memo[row + 1][curInx]
                            accuRow = last[0]
                            removeCol = last[1]
                            memo[row][curInx] = (accuRow + 1, col)
                            if virtual2dArr[row + 1][removeCol - removeColCnts]['attrs']['rowspan'] == "continue":
                                del virtual2dArr[row + 1][removeCol - removeColCnts]
                                removeColCnts += 1
                        else:
                            memo[row][curInx] = (1, col)
                    else:
                        memo[row][curInx] = (0, col)
                curInx += curCell['attrs']['colspan']









        print()



class tr(container):
    __type__ = "tableRow"

    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs": {}}

    def to_json(self, doc) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """

        content = []
        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        self.out['content'] = content

        return self.out


class tc(container):
    __type__ = "tableCell"

    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs": {"colspan": 1, "rowspan": 1}}

    def to_json(self, doc) -> Dict[str, Any]:

        content = []
        for elt in self:
            JSON = elt.to_json(doc)
            if elt.fragment.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcPr':
                content.append(JSON)
            else:
                self.out["attrs"].update(JSON)

        self.out['content'] = content

        return self.out


class tcPr(container):
    __type__ = "tcPr"

    def to_json(self, doc) -> Dict[str, Any]:
        out = {}

        for elt in self:
            res = elt.to_json(doc)
            out.update(res)

        return out


class vMerge(el):
    def to_json(self, doc) -> Dict[str, Any]:
        out = {}
        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        if val:
            out["rowspan"] = val

        return out


class gridSpan(el):
    def to_json(self, doc) -> Dict[str, Any]:
        out = {}

        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        if val:
            out["colspan"] = int(val)

        return out
