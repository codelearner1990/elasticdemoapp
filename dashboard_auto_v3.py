import json
import uuid
import os

def update_objects_and_ids(file_path, new_dataview_name, new_dashboard_title):
    objects = []
    with open(file_path, 'r') as file:
        for line in file:
            objects.append(json.loads(line))

    id_map = {}

    for obj in objects:
        # Generate new IDs for each object
        if 'id' in obj:
            old_id = obj['id']
            new_id = str(uuid.uuid4())
            id_map[old_id] = new_id
            obj['id'] = new_id

            # Update index-pattern name and title
            if obj.get('type') == 'index-pattern' and 'attributes' in obj:
                obj['attributes']['name'] = new_dataview_name
                obj['attributes']['title'] = new_dataview_name

            # Update dashboard title
            if obj.get('type') == 'dashboard' and 'attributes' in obj:
                obj['attributes']['title'] = new_dashboard_title

    # Update references with new IDs
    for obj in objects:
        if 'references' in obj:
            for reference in obj['references']:
                if reference['id'] in id_map:
                    reference['id'] = id_map[reference['id']]

    new_file_name = file_path.replace('.ndjson', '_updated.ndjson')
    with open(new_file_name, 'w') as new_file:
        for obj in objects:
            json.dump(obj, new_file)
            new_file.write('\n')

    print(f"Updated NDJSON file saved to: {new_file_name}")

file_path = '/Users/bhargavsutapalli/Documents/github/elasticrepo/elasticdemoservice_dashboard.ndjson'
new_dataview_name = 'elasticdemonew-logs'
new_dashboard_title = 'elasticdemonew_dashboard'
update_objects_and_ids(file_path, new_dataview_name, new_dashboard_title)
