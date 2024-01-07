from data.namespaces import namespacesData
import json

print(json.dumps([ns.to_dict() for ns in namespacesData]))