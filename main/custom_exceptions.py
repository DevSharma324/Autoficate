
class MainProjectError(Exception):
    """Base Class for all Custom Errors in the Main Project"""


class SessionValuesNotFoundError(MainProjectError):
    """The Session Values are Not Available"""
    
class SimilarItemHeadingError(MainProjectError):
    """The Item Headings Should be Unique"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.form_name = kwargs.get("form_name")
    
class SimilarItemHeadingDataError(MainProjectError):
    """The Item Headings already Exists and Contains Data Set"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.old_data = kwargs.get("old_data")
        self.new_data = kwargs.get("new_data")
        
        print(self.old_data)
        print(self.new_data)

class HeaderDataNotFoundError(MainProjectError):        # TODO: load a page with GET in exception_handler
    """The Current Item Header is Missing"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.form_name = kwargs.get("form_name")

class TableNotFoundError(MainProjectError):
    """Table was not Found in the Excel FIle"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.form_name = kwargs.get("form_name")
