# Helper script to upload artifacts to Nexus

## Usage
```aidl
usage: nexus_uploader.py [-h] -d DIR -n URL -r REPO [-i ID]

Helper script to upload artifacts to Nexus

  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory consisting artifacts to upload
  -n URL, --url URL     Nexus server url
  -r REPO, --repo REPO  Nexus Repository name to upload
  -i ID, --id ID        repo-id defined in settings.xml which contains nexus
                        credentials. Defaults to 'nexus'
```

## Example
```aidl
python nexus_uploader.py --d /Users/siddesh.gurusiddappa/Downloads/tmp/blah -n https://myorg.nexus.com -r blah-poc
```

