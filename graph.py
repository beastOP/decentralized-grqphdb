import copy
from typing import Dict, List
from random import randint
import sys

def priority_sort(priorities: Dict[str, int], data):
    new_args = []
    for i in data:
        weight = priorities[i[0]]
        temp = list(i).copy()
        temp.append(weight)
        new_args.append(temp)
    new_args.sort(key = lambda x: x[-1])
        
    result = map(lambda x: x[:-1], new_args)
    return list(result)


def pprint(value, htchar='    ', lfchar='\n', indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + pprint(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is list:
        items = [
            nlch + pprint(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is tuple:
        items = [
            nlch + pprint(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)

# Create a tree node
class TreeNode(object):
    def __init__(self, key, prop={}):
        self.key = key
        self.prop = prop
        self.left = None
        self.right = None
        self.height = 1

class AVLTree(object):
    def __init__(self):
        self.keys = set()

    # Function to insert a node
    def insert_node(self, root, key, prop={}):
        prop = prop.copy()
        self.keys.add(key)
        if not root:
            return TreeNode(key, prop)
        elif key < root.key:
            root.left = self.insert_node(root.left, key, prop)
        else:
            root.right = self.insert_node(root.right, key, prop)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to delete a node
    def delete_node(self, root, key):
        # Find the node to be deleted and remove it
        if key in self.keys:
            self.keys.remove(key)
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete_node(root.left, key)
        elif key > root.key:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.delete_node(root.right,
                                          temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    # Function to perform left rotation
    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)
    
    def search(self, root, key):
        if (root is None):
            return False
        elif (root.key == key):
            return root
        elif(root.key < key):
            return self.search(root.right, key)
        return self.search(root.left, key)

    def properties(self, root, key):
        item = self.search(root, key)
        if not item:
            return {}
        return item.prop

    def lookup_prop(self, root, key, s, v):
        output = []
        data = [ self.properties(root, i) for i in self.keys if i >= key]
        for i in data:
            if s in i.keys():
                if i[s] == v:
                    output.append(i)
        return output

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

class Database:
    def __init__(self, _id):
        self.id = _id
        self.root = None
        self.nodes = AVLTree()
        self.lables = {}
        self.rkeys = set()
        self.relation_lables = {}
        self.relations = {}

    def gen_weights(self, data):
        weight = []
        for val in data:
            if type(val) == str:
                weight.append(len(val))
            elif type(val) == int:
                weight.append(val)
            elif type(val) == dict:
                weight.append(sum(self.gen_weights(val.values())))
            else:
                weight.append(sum(self.gen_weights(val)))
        return weight

    def add_node(self, data, *args):
        data = data.copy()
        idx = sum(self.gen_weights(data.values()))
        while idx in self.nodes.keys:
            idx = idx + 1
        for i in args:
            if i in self.lables.keys():
                self.lables[i].append(idx)
            else:
                self.lables[i] = [idx]
        data["lables"] = list(args)
        data["bid"] = "%s-%s" % (self.id, idx)
        data["type"] = "node"
        data["relations"] = {}
        self.root = self.nodes.insert_node(self.root, idx, data)
        return "%s-%s" % (self.id, idx)

    """
    db.add_relation(1, 2, {
        timestamp: 943,
    }, "tweet")
    node 1 = {
        bid: 1,
        type: "node",
        properties: {...}
        lables: [...]
        relations: {
            tweets: [1]
        }
    }

    relations 1 = {
        rid: 1,
        from: aux-1,
        to: bx-2,
        properties: {...},
        lables: [...]
    }

    relations_lables = {
        tweets: [1]
    }
    """
    def add_relation(self, _from, to, data = {}, *args):
        print(_from)
        print(to)
        if type(_from) == str:
            _from = int(_from.split("-")[1])
        if type(to) == str:
            to = int(to.split("-")[1])
        _from = self.nodes.search(self.root, _from)
        to = self.nodes.search(self.root, to)
        if not _from or not to or _from == to:
            return False
        idx = sum(self.gen_weights(data.values()))
        if idx in self.rkeys:
            idx += 1
        nr = {
            "rid": idx,
            "from": _from.prop["bid"],
            "to": to.prop["bid"],
            "properties": data,
            "lables": list(args)
        }
        # r
        self.rkeys.add(idx)
        self.relations[idx] = nr
        rl = {}
        for i in args:
            if i in self.relation_lables.keys():
                self.relation_lables[i].append(idx)
            else:
                self.relation_lables[i] = [idx]
            if i in rl.keys():
                rl[i].append(idx)
            else:
                rl[i] = [idx]
        new_data = {
            "relations": rl
        }
        old_props = _from.prop
        old_props.update(new_data)
        if type(_from.prop["bid"]) == str:
            bid = int(_from.prop["bid"].split("-")[1])
        else:
            bid = _from.prop["bid"]
        # r
        _from.prop = old_props
        return idx

    def get_relation(self, key):
        return self.relations(key)

    def delete_node(self, key):
        if type(key) == str:
            key = int(key.split("-")[1])
        prop = self.nodes.properties(self.root, key)
        self.root = self.nodes.delete_node(self.root, key)
        for l in prop["lables"]:
            self.lables[l].remove(key)
        return True
    
    def remove_relation(self, _from, key):
        if type(_from) == str:
            _from = int(_from.split("-")[1])
        from_props = self.nodes.search(self.root, _from).prop
        delete_from = []
        # dct = {}
        for relation in from_props["relations"].keys():
            self.relation_lables[relation].remove(key)
            from_props["relations"][relation].remove(key)
            delete_from.append(relation)

        for relation in delete_from:
            if not len(from_props["relations"][relation]):
                del from_props["relations"][relation]
        #    fltrd = []
        #    for rel in from_props["relations"][relation]:
        #        if key not in rel.values():
        #            fltrd.append(rel)
        #    dct[relation] = fltrd
        #
        #for i in dct.keys():
        #    fltrd = dct[i]
        #    if not len(fltrd):
        #        del from_props["relations"][i]
        #    else:
        #        from_props["relations"][i] = fltrd
        #
        del self.relations[key]
        return True

    def update_node(self, key, data={}, *args):
        if type(key) == str:
            key = int(key.split("-")[1])
        data = data.copy()
        if not data:
            return
        old_data = self.nodes.properties(self.root, key)
        old_lables = old_data["lables"]
        bid = old_data["bid"]
        if type(bid) == str:
            bid = int(bid.split("-")[1])
        rl =  old_data["relations"]
        self.delete_node(key)
        del old_data["lables"]
        del old_data["type"]
        del old_data["bid"]
        del old_data["relations"]
        old_data.update(data)
        idx = sum(self.gen_weights(old_data.values()))
        while idx in self.nodes.keys:
            idx += 1
        for i in old_lables + list(args):
            if i in self.lables.keys():
                self.lables[i].append(idx)
            else:
                self.lables[i] = [idx]
        old_data["lables"] = old_lables + list(args)
        old_data["bid"] = "%s-%s" % (self.id, idx)
        old_data["type"] = "node"
        old_data["relations"] = rl
        self.root = self.nodes.insert_node(self.root, idx, old_data)
        return "%s-%s" % (self.id, idx)
    
    def update_relation(self, key, data, *args):
        pass
    
    def __get_node_by_prop__(self, k, v):
        if type(v) == str:
            key = len(v)
        else:
            key = v
        return self.nodes.lookup_prop(self.root, key, k, v)

    def match(self, *args):
        if not len(args):
            return [ self.nodes.properties(self.root, i) for i in self.nodes.keys ]
        output = []
        ## node > relation > lable > property
        priority = {
            "node": 1,
            "relation": 2,
            "lable": 3,
            "property": 4
        }
        parsed_args = {}

        for i in args:
            if i[0] in parsed_args.keys():
                parsed_args[i[0]].append(i)
            else:
                parsed_args[i[0]] = [i]

        for i in parsed_args.keys():
            prsd = {}

            if i == "lable":
                for j in parsed_args[i]:
                    if j[1] in prsd.keys():
                        prsd[j[1]].append(j[2])
                    else:
                        prsd[j[1]] = [j[2]]
            elif i == "property":
                for j in parsed_args[i]:
                    if j[2] in prsd.keys():
                        prsd[j[2]].append({ j[1]: j[3]})
                    else:
                        prsd[j[2]] = [{ j[1]: j[3]}]

            parsed_args[i] = prsd

        if "lable" in parsed_args.keys():
            for key in parsed_args["lable"].keys():
                if key == "is":
                    lables = []
                    h = parsed_args["lable"]["is"]
                    for i in h:
                        lables += self.lables[i]
                    output += [ self.nodes.properties(self.root, k) for k in lables ]
                elif key == "is not":
                    lables = []
                    h = parsed_args["lable"]["is not"]
                    for i in self.lables.keys():
                        if i not in h:
                            lst = []
                            for l in self.lables[i]:
                                tmp = self.nodes.properties(self.root, l)["lables"]
                                if i not in tmp:
                                    lst.append(tmp)
                            lables += lst
                    output += [ self.nodes.properties(self.root, k) for k in lables ]

        if "property" in parsed_args.keys():
            for key in parsed_args["property"].keys():
                if key == "is":
                    for k in parsed_args["property"][key]:
                        for j in k.keys():
                            if "lable" not in parsed_args.keys():
                                dta = self.__get_node_by_prop__(j, k[j])
                                output += dta 
                            else:
                                lst = []
                                for i in output:
                                    if i[j] == k[j]:
                                        lst.append(i)
                                output = lst

                elif key == "is not":
                    for k in parsed_args["property"][key]:
                        for j in k.keys():
                            if "lable" not in parsed_args.keys():
                                bids = [ m["bid"] for m in self.__get_node_by_prop__(j, k[j]) ]
                                output = [self.nodes.properties(self.root, f) for f in self.nodes.keys if f not in bids]
                            else:
                                bids = [ m["bid"] for m in output if m[j] != k[j] ]
                                output = [self.nodes.properties(self.root, f) for f in self.nodes.keys if f in bids]

        # Removing duplicates
        output = [i for n, i in enumerate(output) if i not in output[n + 1:]]
        return output

    def print_nodes(self):
        self.nodes.printHelper(self.root, "", True)


"""
[{
    bid: 1,
    type: "node",
    properties: {
        ...
    },
    lables: ["premium", "verified"]
    relations: {
        tweets: [{
            rid: 1,
            type: "relation",
            # from: 1,
            to: 2,
            properties: {
                ...
            },
            lables: ["popular_tweets", "trending_tweets"]
        }]
    }
}]
"""
if __name__ == "__main__":
    data = {
        "name": "Omkar",
        "age": 19
    }
    db = Database("Aux7")
    db.add_node(data, "user")
    id1 = db.add_node(data, "user", "self")
    # db.delete_node(25)
    # print("#### After Deletion ####")
    # print(pprint(db.match(("property", "name", "is", "Omkar"))))
    # print("#### After updating ####")
    data.update({
        "name": "shubham",
        "age": 22
    })
    id2 = db.update_node(24, data, "hero")
    db.add_relation(id2, id1, {}, "brother")
    key = db.add_relation(id1, id2, {}, "brother")
    # print(pprint(db.match(("lable", "is", "user"), ("property", "name", "is", "Omkar"), ("property", "age", "is", 19))))
    print(pprint(db.match()))
    db.remove_relation(id1, key)
    print(pprint(db.match()))
    print(db.nodes.keys)
    print(db.lables)
    print(db.relations)
    print(db.relation_lables)
    # db.print_nodes()
    # print(pprint(db.match(("property", "name", "is", "Omkar"))))
