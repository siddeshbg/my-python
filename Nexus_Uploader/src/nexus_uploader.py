import os
from subprocess import call
from argparse import ArgumentParser
import sys
from lxml import etree


class NexusUploader:
    def __init__(self, root_dir, nexus_url, nexus_repo, repo_id='nexus'):
        self.root_dir = root_dir
        self.nexus_url = nexus_url
        self.nexus_repo = nexus_repo
        self.repo_id = repo_id

    def get_pom_files(self):
        poms = []

        for dir_name, subdir_list, file_list in os.walk(self.root_dir):
            for file_name in file_list:
                if file_name.endswith('.pom'):
                    poms.append(os.sep.join([dir_name, file_name]))

        return poms

    def upload_with_poms(self):
        poms = self.get_pom_files()
        parser = etree.XMLParser(remove_comments=False)

        for index, pom in enumerate(poms):
            print("%d/%d: %s" % (index + 1, len(poms), pom))

            for file in os.listdir(os.path.dirname(pom)):
                if file.endswith(".jar") and "-sources" in file:
                    source_file = os.path.join(os.path.dirname(pom), file)
                elif file.endswith(".jar"):
                    jar_file = os.path.join(os.path.dirname(pom), file)

            xml = etree.parse(pom, parser=parser)
            groupId = xml.find("./{*}groupId")
            artifactId = xml.find("./{*}artifactId")
            version = xml.find("./{*}version")
            packaging = xml.find("./{*}packaging")
            if not packaging:
                packaging = "jar"
            else:
                packaging = packaging.text

            print("Running CMD: mvn deploy:deploy-file -DgeneratePom=false -DgroupId=%s -DartifactId=%s -Dversion=%s "
                "-Dpackaging=%s -Dfile=%s -DrepositoryId=%s -Durl=%s/repository/%s -DpomFile=%s -Dsources=%s -DuniqueVersion=false"
                % (groupId.text, artifactId.text, version.text, packaging, jar_file, self.repo_id, self.nexus_url,
                   self.nexus_repo, pom, source_file))

            call("mvn deploy:deploy-file -DgeneratePom=false -DgroupId=%s -DartifactId=%s -Dversion=%s -Dpackaging=%s "
                 "-Dfile=%s -DrepositoryId=%s -Durl=%s/repository/%s -DpomFile=%s -Dsources=%s -DuniqueVersion=false"
                 % (groupId.text, artifactId.text, version.text, packaging, jar_file, self.repo_id, self.nexus_url,
                    self.nexus_repo, pom, source_file), shell=True)

def main():
    parser = ArgumentParser(description='Helper script to upload artifacts to Nexus')
    parser.add_argument("-d", "--dir", help='Directory consisting artifacts to upload', required=True)
    parser.add_argument("-n", "--url", help='Nexus server url', required=True)
    parser.add_argument("-r", "--repo", help='Nexus Repository name to upload', required=True)
    parser.add_argument("-i", "--id", help='repo-id defined in settings.xml which contains nexus credentials.'
                                           "Defaults to 'nexus'")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    root_dir = args.dir
    nexus_url = args.url
    nexus_repo = args.repo

    if not os.path.isdir(root_dir):
        print("[ERROR] %s dir not found" % root_dir)
        exit(1)

    if args.id is not None:
        repo_id = args.id
        uploader = NexusUploader(root_dir, nexus_url, nexus_repo, repo_id)
    else:
        uploader = NexusUploader(root_dir, nexus_url, nexus_repo)

    uploader.upload_with_poms()


if __name__ == '__main__':
    main()
