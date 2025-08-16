import json

def validate_software_list(software_list_file):
    with open(software_list_file, 'r') as file:
        software_list = json.load(file)
    
    required_fields = ["name", "english_name", "app_id", "knotlink_version", "description", "url", "status"]
    
    for software in software_list:
        for field in required_fields:
            if field not in software:
                print(f"Error: {field} is missing in {software.get('name', 'unknown')}")
                return False
            if field == "knotlink_version" and not isinstance(software[field], str):
                print(f"Error: {field} must be a string in {software.get('name', 'unknown')}")
                return False
            if field == "status" and software[field] not in ["stable", "development", "deprecated"]:
                print(f"Error: {field} must be one of 'stable', 'development', 'deprecated' in {software.get('name', 'unknown')}")
                return False
    print("All software entries are valid.")
    return True

# 示例：验证软件清单
validate_software_list('software_list.json')