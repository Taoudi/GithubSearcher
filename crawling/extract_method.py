# # http = urllib3.PoolManager()
# codes = []
# urls = []
# programs = []
# clean_code = []
# class_names = []
# index = {'code': [],'name':[]}

class Code:
    def __init__(self, functions, codeblock, url):
        self.codeblock = codeblock
        self.functions = functions
        self.url = url

    def jsonify(self):
        string = "{ url:" + self.url.replace('\n', '') + ",\nfunctions:" + "["
        for i, f in enumerate(self.functions):
            string += f.jsonify()
            if i < len(self.functions) - 1:
                string += ",\n "

        string += "]" + ",\ncodeblock:{\"\"\"\n" + self.codeblock + "\n\"\"\"}\n}"
        return string


class Parameter:
    def __init__(self, name, v_type):
        self.name = name
        self.type = v_type

    def jsonify(self):
        return "{ 'name':" + self.name + ",'type" + self.type + "}"

    def __str__(self):
        return self.name + " " + self.type


class Method:
    def __init__(self, access_modifier="", static=False, return_type="", method_name="", parameters=list()):
        self.access_modifier = access_modifier
        self.static = static
        self.return_type = return_type
        self.method_name = method_name
        self.parameters = parameters

    def __str__(self):
        string = self.access_modifier
        if self.static:
            string += " " + "static"
        string += " " + self.return_type + " " + self.method_name + "("
        if len(self.parameters) == 0:
            return string + ")"
        elif len(self.parameters) == 1:
            return string + str(self.parameters[0]) + ")"
        else:
            for i, p in enumerate(self.parameters):
                string += str(p)
                if i < len(self.parameters) - 1:
                    string += ", "
            return string + ")"

    def jsonify(self):
        string = "{ access_modifier:" + self.access_modifier + ", "
        if self.static:
            string += "static: " + "True, "
        else:
            "static: " + "False, "

        string += "return_type:" + self.return_type + ", method_name:" + self.method_name + ", "
        if len(self.parameters) == 0:
            return string + "parameters:[] }"
        elif len(self.parameters) == 1:
            return string + "parameters:[" + "{ type:" + self.parameters[0].type + ", name:" + self.parameters[
                0].name + "}" + "] }"
        else:
            string += "parameters:["
            for i, p in enumerate(self.parameters):
                string += "{ type:" + p.type + ", name:" + p.name + "}"
                if i < len(self.parameters) - 1:
                    string += ", "
            return string + "] }"
