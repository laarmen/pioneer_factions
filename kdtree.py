class KdTreeNode:
    def __init__(self, el_list, depth=0):
        if not el_list:
            raise ValueError
     
        # Useful when removing a large number of item
        self.removal_flag = False

        # Sort el list and choose median as pivot element
        el_list.sort(key=lambda el: el.dimension(depth))
        median = len(el_list) / 2 # choose median
     
        # Create node and construct subtrees
        self.element = el_list[median]
        try:
            self.left_child = KdTreeNode(el_list[:median], depth + 1)
        except ValueError:
            self.left_child = None
        try:
            self.right_child = KdTreeNode(el_list[median + 1:], depth + 1)
        except ValueError:
            self.right_child = None

    def add(self, el, depth=0):
        if el == self.element:
            return
        if el.dimension(depth) <= self.element.dimension(depth):
            if self.left_child == None:
                self.left_child = KdTreeNode([el], depth+1)
            else:
                self.left_child.add(el, depth+1)
        else:
            if self.right_child == None:
                self.right_child = KdTreeNode([el], depth+1)
            else:
                self.right_child.add(el, depth+1)

    def remove(self, el, depth=0):
        if self.element != el:
            if el.dimension(depth) <= self.element.dimension(depth):
                if self.left_child != None:
                    self.left_child.remove(el, depth+1)
            else:
                if self.right_child != None:
                    self.right_child.remove(el, depth+1)
            return
        self.removal_flag = True
        self.cleanup(depth)

    def cleanup(self, depth = 0):
        if not self.removal_flag:
            if self.left_child != None:
                self.left_child.cleanup(depth+1)
            if self.right_child != None:
                self.right_child.cleanup(depth+1)
        node = KdTreeNode(self.list_el(), depth)
        self.element = node.location
        self.left_child = node.left_child
        self.right_child = node.right_child

    def list_el(self):
        els = []
        if not self.removal_flag: els.append(self.element)
        if self.left_child != None:
            els.extend(self.left_child.el_list())
        if self.right_child != None:
            els.extend(self.right_child.el_list())
        return els

    def mark_if_predicat(self, predicat, depth=0):
        try:
            self.removal_flag = predicat(self.element, depth)
        except ValueError:
            return
        if self.left_child != None:
            self.left_child.mark_if_predicat(predicat, depth+1)
        if self.right_child != None:
            self.right_child.mark_if_predicat(predicat, depth+1)

    def subset(self, inclusion_predicat, recursion_predicat, depth = 0):
        '''inclusion_predicat : 2 args : element, depth
        recursion_predicat : 2 args : element, depth
        The inclusion predicat determines whether this particular node should be included in the subset.
        The recursion predicat returns the branches on which there is potentially other members.
        '''
        subset = []
        if inclusion_predicat(self, depth):
            subset.append(self.element)
        next_nodes = recursion_predicat(self, depth)
        for n in next_nodes:
            subset.extend(n.subset(inclusion_predicat, recursion_predicat, depth+1))
        return subset

    def hypercube(self, side_length, center, dimension):
        u'''
        side_length: the length of a side of the hypercube.
        center: The element in the center of the hypercube.
        dimension: the dimension the hypercube is in. For a square, it would be 2, a cube, 3.
        '''
        inc_pred = lambda n, depth: \
            reduce(lambda a, b: a and b,
                   map(lambda i:
                           abs(n.element.dimension(i) - center.dimension(i)) < side_length/2.,
                       range(dimension)),
                   True)

        def rec_pred(n, depth):
            diff = n.element.dimension(depth) - center.dimension(depth)
            return_list = []
            if diff > -side_length/2. and n.left_child:
                return_list.append(n.left_child)
            if diff < side_length/2. and n.right_child:
                return_list.append(n.right_child)
            return return_list
        return self.subset(inc_pred, rec_pred)

