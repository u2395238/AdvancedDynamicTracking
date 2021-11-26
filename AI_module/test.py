#linked list
class node:
    def __init__(self, val):
        self.val=val
        self.next=None

class ll:
    def __init__(self):
        self.head = None
    
    def Insert(self, data):
        end = self.head
        Newnode = node(data)
        if(self.head is None):
            self.head=Newnode
        else:
            while(end.next is not None):
                end = end.next
        end.next = Newnode
    
    
    def display(self):
        data=self.head
        while(data.next is not None):
            print(data.val)
            data = data.next
            # hello there yoo



l = ll()
l.Insert('srh')
l.display()
