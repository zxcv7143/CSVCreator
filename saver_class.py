import pickle
import os


class SaverClass():
    def __init__(self, param):
        self.param = param

    def save_user(obj):
        try:
            with open("user.pickle", "wb") as f:
                pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            pass
            #print("Error during pickling object (Possibly unsupported):", ex)

    def load_user():
        try:
            with open("user.pickle", "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            pass
            #print("Error during unpickling object (Possibly unsupported):", ex)

    def load_default_type():
        try:
            with open("type.pickle", "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            pass
            #print("Error during unpickling object (Possibly unsupported):", ex)

    def save_default_type(type):
        try:
            with open("type.pickle", "wb") as f:
                pickle.dump(type, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            pass
            #print("Error during unpickling object (Possibly unsupported):", ex)

    def delete_default_type():
        try:
            if os.path.isfile("type.pickle"):
                os.remove("type.pickle")
        except:
            pass
