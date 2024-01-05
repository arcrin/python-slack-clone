from data.namespaces import namespaces
import json

print(json.dumps([ns.to_dict() for ns in namespaces]))