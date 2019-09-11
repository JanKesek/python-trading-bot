import pickle
class Pickler:
    def __init__(self, name, obj=None):
        self.name=name
        self.obj=obj
    def save(self):
        pickle_out=open("pickleData/" + self.name + ".pickle", "wb")
        pickle.dump(self.obj, pickle_out)
        pickle_out.close()
    def retrieve(self):
        pickle_in=open("pickleData/" + self.name+ ".pickle", "rb")
        return pickle.load(pickle_in)
