SAMPLE_NOT_SELECTED = "sample not selected"
NO_OUTPUT_DATA = "no output data"
SETTINGS_SAVED = "settings saved"

ERROR_PREFIX = "Error"
EXCEL_EXPORT_SUCCESS_PREFIX = "Excel export success"


def excel_export_success(filename):
    return f"{EXCEL_EXPORT_SUCCESS_PREFIX}: {filename}"


def error_message(error):
    return f"{ERROR_PREFIX}: {error}"
