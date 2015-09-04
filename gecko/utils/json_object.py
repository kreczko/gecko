
class JSONObject(object):

    def toDict(self):
        # loop over all attributes
        # convert each attribute into a simple type (number, string, bool)
        # convert each complex object into a dictionary
        # add class name
        d = deepcopy(self.__dict__)
        d['class'] = str(self.__class__)

    def toJSON(self, output_file_name):
        pass

    @staticmethod
    def fromDict(dictionary):
        pass

    @staticmethod
    def fromJSON(file_name):
        pass
