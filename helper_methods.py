class helpers():
    def formatStringField(input):
        stringFields = input.split(",")
        fieldList = ""

        for field in stringFields:
            field = field.strip().strip('\"')
            field = "\"" + field + "\","
            fieldList = fieldList + field
        
        stringFieldsSection = """  json_string_fields = [{value}]\n""".format(value=fieldList)
        return stringFieldsSection