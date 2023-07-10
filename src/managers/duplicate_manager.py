# imports, python
from os import mkdir
from os import stat
from os import walk
from os.path import exists
from pathlib import Path

# imports, project
from config.config import duplicate_search_targets
from config.config import duplicate_size_lookaround


class DuplicateManager:
    def __init__(
            self,
            debug=False
    ):
        self._debug = debug
        self._duplicate_search_targets = duplicate_search_targets
        self._duplicate_size_lookaround = duplicate_size_lookaround

    def run(self):
        self.validate_required_settings_available()
        self.identify_duplicates()

    def validate_required_settings_available(self):
        """
        Check that required values to continue are available.
        """
        if not self._duplicate_search_targets:
            print(f'{self.__class__.__name__} is missing required '
                  f'targets.')
            exit()

        if not self._duplicate_size_lookaround:
            print(f'{self.__class__.__name__} is missing required '
                  f'lookaround value.')
            exit()

    def identify_duplicates(self):
        # Process each target
        for target_label, target_details in self._duplicate_search_targets.items():
            self.process_target(
                label=target_label,
                details=target_details
            )
            pass

    def process_target(self, label, details):
        all_files_at_path = []
        valid = self.validate_keys_in_(details)
        if valid:
            path_to_check = Path(details['path_to_check'])
            path_to_result = Path(details['path_to_result'])
            all_files_at_path = self.read_all_files_at_(path_to_check)
            self.extract_sizes_and_sort(
                label=label,
                all_files_at_path=all_files_at_path
            )
            # TODO write duplicate results to path_to_result

    @staticmethod
    def validate_keys_in_(details) -> bool:
        # Validate enabled
        key = 'enabled'
        if key not in details:
            return False  # Not valid, key missing
        if not details[key]:
            return False  # Not valid, disabled
        del key

        # Validate path to check
        key = 'path_to_check'
        if key not in details:
            return False  # Not valid, key missing
        path_to_check = Path(details[key])
        if not exists(path_to_check):
            return False  # Not valid, path not exist
        del key

        # Validate path to result
        key = 'path_to_result'
        if key not in details:
            return False  # Not valid, key missing
        path_to_result = Path(details[key])
        if not exists(path_to_result):
            try:
                mkdir(path_to_result)
            except Exception as exc:
                print(f'Exception caught : {exc}')
                return False  # Not valid, path creation failed
        del key

        return True  # Validity checks passed

    def read_all_files_at_(self, path_to_check) -> list:
        all_files = []
        for root, dirs, files in walk(path_to_check):
            for file in files:
                path_to_file = Path(root, file)
                if not exists(path_to_file):
                    self.record_invalid_file(path_to_file)
                    continue
                all_files.append(path_to_file)
        return all_files

    def extract_sizes_and_sort(self, label, all_files_at_path):
        fas = files_and_sizes = {}
        for file_at_path in all_files_at_path:
            file_stat = stat(file_at_path)
            if not hasattr(file_stat, 'st_size'):
                continue
            files_and_sizes.update({
                str(file_at_path): file_stat.st_size
            })
        files_and_sizes_sorted = \
            dict(sorted(fas.items(), key=lambda item: item[1],
                        reverse=True))
        setattr(self, label, files_and_sizes_sorted)

    @staticmethod
    def record_invalid_file(path_to_file):
        """It could be nice to keep a list of invalid files that
            failed the os.exists() test to investigate later.
        TODO
        """
        print(f'Invalid file, no action taken : {path_to_file}')
