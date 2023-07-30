# Manage the file metadata

from src.enumerations import CollectionType
from src.enumerations import FileAttribute
from src.enumerations import MetadataKey as mk


class MetadataManager:
    def __init__(self):
        print(f'Init {self.__class__.__name__}')
        self._collection_metadata = {}

    # Parent Properties

    @property
    def collection_metadata(self) -> dict:
        return self._collection_metadata

    @collection_metadata.setter
    def collection_metadata(self, value: dict):
        self._collection_metadata = value

    # Children Properties

    def archive_valid(self, collection_name):
        collection_archive_metadata = (
            self.get_collection_metadata(
                collection_name,
                CollectionType.ARCHIVE))
        if collection_archive_metadata:
            return False
        return True

    @staticmethod
    def delete_entry(metadata: dict, key: str):
        if key not in metadata:
            print(f'Error, {key} not found in metadata')
            return
        del metadata[key]

    def get_collection_file_metadata(
            self,
            collection_name: str,
            file_type: str):
        return self.collection_metadata[
            collection_name][
            mk.FILES][
            file_type]

    def get_collection_metadata(
            self,
            collection_name: str,
            file_type: str) -> dict:
        if file_type == CollectionType.ARCHIVE:
            return self.collection_metadata[
                collection_name][
                mk.FILES][
                CollectionType.ARCHIVE]

    @staticmethod
    def get_file_size_from(
            collection_metadata: dict,
            file: str):
        return collection_metadata[
            file][
            FileAttribute.ST_SIZE]

    def get_files(self, collection_name: str, file_type: str):
        return self.collection_metadata[
            collection_name][
            mk.FILES][
            file_type]

    @staticmethod
    def get_hash(collection_metadata: dict, file: str) -> str:
        return collection_metadata[file][mk.HASH]

    @staticmethod
    def get_parent_count_from(duplicate_metadata: dict):
        return len(duplicate_metadata)

    def init_collection_metadata(
            self,
            collection_name: str,
            collection_paths: dict):
        self.collection_metadata = {
            collection_name: {
                mk.COLLECTION_PATHS: collection_paths}}

    def init_file_metadata(
            self,
            collection_name: str,
            files_at_path: dict,
            path_type: str):
        if mk.FILES not in self.collection_metadata[collection_name]:
            self.collection_metadata[collection_name][mk.FILES] = {}
        if path_type == CollectionType.ARCHIVE:
            self.collection_metadata[collection_name][mk.FILES].update({
                path_type: files_at_path})
        elif path_type == CollectionType.SOURCE:
            self.collection_metadata[collection_name][mk.FILES].update({
                path_type: files_at_path})
        else:
            raise RuntimeError(f'Unknown path_type : {path_type}')

    def set_duplicate_metadata(
            self,
            collection_name: str,
            duplicate_metadata: dict):
        collection_file_metadata = \
            self.collection_metadata[
                collection_name][
                mk.FILES][
                CollectionType.ARCHIVE]
        if duplicate_metadata is None:
            return
        for parent_file, children_files in duplicate_metadata.items():
            collection_file_metadata[parent_file].update({
                mk.DUPLICATES: children_files
            })

    @staticmethod
    def set_soft_link_command(collection_metadata: dict,
                              duplicate_metadata: dict,
                              command: list):
        original = duplicate_metadata[mk.ORIGINAL]
        duplicate = duplicate_metadata[mk.NAME]
        collection_metadata[
            original][
            mk.DUPLICATES][
            duplicate][
            mk.SOFT_LINK_COMMAND] = command

    @staticmethod
    def set_unstage_storage_details(
            collection_metadata: dict,
            duplicate_file_metadata: dict,
            unstage_storage_details: dict):
        unstage_file_dc = duplicate_file_metadata[mk.NAME]
        original_file_dc = duplicate_file_metadata[mk.ORIGINAL]
        collection_metadata[
            original_file_dc][
            mk.DUPLICATES][
            unstage_file_dc].update(unstage_storage_details)

    @staticmethod
    def update_duplicate_metadata(
            new_parent_file: str,
            duplicate_metadata: dict,
            file: str,
            file_metadata: dict):
        if new_parent_file not in duplicate_metadata:
            duplicate_metadata[new_parent_file] = {file: file_metadata}
        else:
            duplicate_metadata[new_parent_file].update({file: file_metadata})

    @staticmethod
    def update_metadata_for_child(
            collection_name: str,
            collection_metadata: dict,
            duplicate_metadata_for_file: dict,
            parent_name: str,
            parent_hash: str,
            child_name: str,
            child_hash: str):
        duplicate_metadata_for_file.update({child_name: {
            mk.COLLECTION: collection_name,
            mk.HASH: child_hash,
            mk.NAME: child_name,
            mk.PARENT: {
                mk.HASH: parent_hash,
                mk.NAME: parent_name,
                mk.SIZE: collection_metadata[parent_name]['ST_SIZE']
            },
            mk.SIZE: collection_metadata[child_name]['ST_SIZE']
        }})

    @staticmethod
    def update_metadata_for_parent(
            parent_file: str,
            parent_metadata: dict,
            child_metadata: dict):
        child_metadata.update({parent_file: parent_metadata })

    def update_file_hashes(
            self,
            collection_name: str,
            file_type: str,
            file_hashes: dict) -> None:
        files = self.collection_metadata[collection_name][mk.FILES][file_type]
        for file, file_details in files.items():
            file_details.update({
                mk.HASH: file_hashes[file][mk.HASH]
            })
