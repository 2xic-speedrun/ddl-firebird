from ..definitions.Trigger import Trigger
from ..FirebirdParser import FirebirdParser

class TransformTrigger:
    def __init__(self):
        pass

    def transform(self, code):
        """
        This is not a true transformer,
        I just want to inject code before a call to the trigger
        Namely a call to a logging procedure with the name of the trigger

        EXECUTE PROCEDURE (Proecedure_NAME)
            -> Proecedure takes care of logging the metadata
        """
        parser = FirebirdParser(code)
        (results, streamer) = Trigger().parse(parser.streamer)
        print(results.name)
        print(results.name)
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
