from ..definitions.Trigger import Trigger
from ..definitions.Procedure import Procedure
from ..FirebirdParser import FirebirdParser

class TransformProcedure:
    def __init__(self):
        pass

    def transform(self, code):
        """
        This is not a true transformer,
        I just want to inject code before a call to the procedure
        Namely a call to a logging procedure with the name of the Proecedure

        EXECUTE PROCEDURE (Proecedure_NAME)
            -> Proecedure takes care of logging the metadata
        """
        parser = FirebirdParser(code)
        (results, streamer) = Procedure().parse(parser.streamer)
        print(results.name)

        keyword = self._find_keyword(code, "BEGIN")
#        print(results)
        transformed_code = code.replace(keyword, f"BEGIN\nEXECUTE PROCEDURE ADD_DEBUG_INFO ('{results.name}');\n", 1)
        return transformed_code

    def _find_keyword(self, content, keyword):
        if keyword.lower() in content and keyword.upper() in content:
            if content.index(keyword.lower()) < content.index(keyword.upper()):
                return keyword.lower()
            return keyword.upper()
        elif keyword.lower() in content:
            return keyword.lower()
        else:
            return keyword.upper()
