class Utilities():
    """
    Class that stores useful utility functions that may be needed across the code base
    """
    
    def catch_exception(self, func, *args, **kwargs):
        """
        Used to catch exceptions when the function is being used in a comprehension
        """
        try:
            return func(*args, **kwargs)
        except:
            return 'error'



class DictObjectView(object):
    """
    simply used to wrap a dictionary in an obj so as can use dot notation to access 
    the dict entries.
    """

    def __init__(self, dict):
        self.__dict__ = dict


