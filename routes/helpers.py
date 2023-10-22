def listErrors(formErrors):
    error = ""
    for key, value in formErrors.items():
        error += key + ": " + value[0] + "\n"
    return error
