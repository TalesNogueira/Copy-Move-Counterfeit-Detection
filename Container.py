class Container(object):
    def __init__(self):
        """
        Starts an container object used to store multiple data.
        """
        self.container = []

    def appendContainer(self, data):
        """
        Append data to the end of the container list.
        'data': data to be stored
        """
        self.container.append(data)

    def sortByPCA(self):
        """
        Sort the container of blocks by the PCA in crescent order.
        """
        self.container = sorted(self.container, key = lambda x:x[1])

    def getLenght(self):
        """
        Get container lenght; returns container lenght.
        """
        return self.container.__len__()