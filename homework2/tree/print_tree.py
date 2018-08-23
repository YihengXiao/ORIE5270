
class Node(object):
    def __init__(self, value, left, right):
        """
        Initialize Node
        :param value: value of node
        :attrib left: left node
        :attrib right: right node
        """
        self.value = value
        self.left = left
        self.right = right


class Tree(Node):
    def __init__(self, root):
        self.root = root

    @classmethod
    def PrintTree(cls, root):
        if not root:
            return ""
        q = [root]
        res = [[root]]
        while q:
            x = []  # record next level (children) = q
            for item in q:
                if item.left is not None and item.left.value != "*":
                    x.append(item.left)
                else:
                    x.append(Node('*', None, None))
                if item.right is not None and item.right.value != "*":
                    x.append(item.right)
                else:
                    x.append(Node('*', None, None))
            q = x
            if len(q) > 0 and len(list(filter(lambda y: y.value != '*', q))) > 0:
                res.append(q)
            else:
                break
        for i in range(len(res)):
            for j in range(len(res[i])):
                if res[i][j].value in [None, "*"]:
                    res[i][j] = "*"
                else:
                    res[i][j] = res[i][j].value

        n = len(res)
        out = ""
        for i in range(1, len(res)+1):
            side = "|"*(2**(n-i)-1)
            if 2**(i-1)-1 > 0:
                sep = int(((2**n-1)-(2**(n-i)-1)*2-2**(i-1))/(2**(i-1)-1))
            else:
                sep = 0
            sep = "|"*sep
            out += side
            for j in range(len(res[i-1])):
                if j != len(res[i-1])-1:
                    if res[i-1][j] != "*":
                        out += str(res[i-1][j])
                        out += sep
                    else:
                        out += "|"
                        out += sep
                else:
                    if res[i-1][j] != "*":
                        out += str(res[i-1][j])
                    else:
                        out += "|"
            out += side
            out += "\n"
        return out
