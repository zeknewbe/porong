import xml.etree.ElementTree as ET
import requests
import os

GITHUB_REPO_API = 'https://api.github.com/repos/zeknewbe/porong/contents/merged_epg.xml'

def fetch_xml(url):
    response = requests.get(url)
    return ET.ElementTree(ET.fromstring(response.text))

def merge_trees(tree1, tree2):
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    for child in root2:
        root1.append(child)

    return tree1

def write_to_github(content, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Fetch the file to get the SHA (needed for updating an existing file)
    response = requests.get(GITHUB_REPO_API, headers=headers)
    sha = response.json().get('sha', '')

    data = {
        "message": "Updated merged EPG file",
        "content": content.encode('utf-8').decode('latin1'),  # GitHub requires base64 content
        "sha": sha
    }

    response = requests.put(GITHUB_REPO_API, headers=headers, json=data)
    if response.status_code == 201:
        print("File successfully updated!")
    else:
        print(f"Failed to update. Status Code: {response.status_code}. Response: {response.text}")

if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not set!")
        exit(1)

    tree1 = fetch_xml('https://i.mjh.nz/PlutoTV/cl.xml')
    tree2 = fetch_xml('https://i.mjh.nz/Plex/mx.xml')

    merged_tree = merge_trees(tree1, tree2)
    merged_xml = ET.tostring(merged_tree.getroot(), encoding='utf-8').decode('utf-8')

    write_to_github(merged_xml, token)
