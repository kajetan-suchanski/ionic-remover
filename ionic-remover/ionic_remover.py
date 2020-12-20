import os
import os.path as path
import shutil
from typing import Optional, List

from colored_terminal import print_blue, print_green, print_pink
from config import *
from naming_convention import NamingConvention
from regex import REGEX_CLASS_NAME, REGEX_ELEMENT, REGEX_CAPITAL_LETTER, get_import_regex
from result_element import ResultElement
from templates import Templates


class IonicRemover:
    generated_directory: str
    file_extensions: List[str]
    copy_all_files: bool
    convert_to: ResultElement
    element_prefix: str
    naming_convention: NamingConvention
    generate_elements: bool
    remove_capacitor: bool

    created_elements = set()

    def __init__(self, generated_directory=DEFAULT_GENERATED_DIRECTORY, file_extensions: Optional[List[str]] = None,
                 copy_all_files=True, convert_to=ResultElement[DEFAULT_CONVERT_TO], element_prefix="",
                 naming_convention: Optional[NamingConvention] = None, remove_capacitor=True):

        self.generated_directory = generated_directory

        if file_extensions is None:
            self.file_extensions = DEFAULT_FILE_EXTENSIONS
        else:
            self.file_extensions = file_extensions

        self.copy_all_files = copy_all_files
        self.convert_to = convert_to
        self.element_prefix: str = element_prefix

        if naming_convention is None:
            self.naming_convention = NamingConvention.KEBAB_CASE \
                if convert_to == ResultElement.DIV \
                else NamingConvention.CAMEL_CASE

        else:
            self.naming_convention = naming_convention

        self.generate_elements = convert_to == ResultElement.REACT_COMPONENT
        self.remove_capacitor = remove_capacitor

    def remove_ionic_from_react_file(self, root: str, file: str, dst_root: str):
        src_path = path.join(root, file)
        with open(src_path, "rt") as fin:
            content = fin.read()

        dst_path = path.join(dst_root, file)
        with open(dst_path, "wt") as fout:
            content = self.remove_imports(content)
            content = self.replace_components(content)
            fout.write(content)

    def remove_ionic_from_react_project(self, ionic_dir: str, dst_dir: str):
        ionic_dir = path.abspath(ionic_dir)
        dst_dir = path.abspath(dst_dir)

        if ionic_dir == dst_dir:
            raise ValueError("Ionic source directory and destination directory must not be the same.")

        n_files = 0
        for root, sub_dirs, files in os.walk(ionic_dir):

            dst_root = path.join(dst_dir, root[len(ionic_dir) + 1:])
            if not path.exists(dst_root):
                os.makedirs(dst_root)

            for file in files:
                if file.endswith(tuple(self.file_extensions)):
                    print("Processing\t" + path.join(path.abspath(root), file))
                    self.remove_ionic_from_react_file(root, file, dst_root)
                    print_blue("Saved to\t" + path.join(path.abspath(dst_root), file))
                    n_files += 1

                elif self.copy_all_files:
                    src_file = path.join(root, file)
                    dst_file = path.join(dst_root, file)
                    shutil.copy(src_file, dst_file)

        print_green("\n" + str(n_files), "source files are ionic-free now." + "\n")

        if self.convert_to == ResultElement.DIV:
            what_created = "classes"
        else:
            what_created = "components"

        print_pink(str(len(self.created_elements)), what_created, "has been defined:")

        if self.generate_elements and not path.exists(self.get_generated_directory(dst_dir)):
            os.makedirs(self.get_generated_directory(dst_dir))

        for created_element in self.created_elements:
            print(created_element)
            if self.generate_elements:
                self.create_generated_element_file(dst_dir, created_element)

    def element_sub(self, match):
        if match.group(1):
            if self.convert_to == ResultElement.DIV:
                return "</div>"
            else:
                return "</" + self.convert_name(match.group(2)[3:]) + ">"

        else:
            element_name = self.convert_name(match.group(2)[3:])
            self.created_elements.add(element_name)
            props: str = match.group(3)
            if self.convert_to == ResultElement.REACT_COMPONENT:
                return "<" + element_name + props + ">"

            # add tag name to classes set
            # if the element already has a `className` property
            if "className=" in props.replace(r"\s", ""):
                props = REGEX_CLASS_NAME.sub(r"\1" + element_name + " ", props)
            # create `className` property otherwise
            else:
                props = "className=\"" + element_name + "\"" + props

            return "<div " + props + ">"

    def remove_imports(self, content: str):
        return get_import_regex(self.remove_capacitor).sub("", content)

    def replace_components(self, content: str):
        return REGEX_ELEMENT.sub(lambda match: self.element_sub(match), content)

    def convert_name(self, element_name: str):
        if self.naming_convention == NamingConvention.KEBAB_CASE and self.convert_to == ResultElement.DIV:

            element_name = REGEX_CAPITAL_LETTER.sub(lambda match: "-" + match.group(0).lower(), element_name)
            if len(self.element_prefix) == 0:
                element_name = element_name[1:]

        elif len(self.element_prefix) > 0:
            self.element_prefix = self.element_prefix.capitalize()

        return self.element_prefix + element_name

    def create_generated_element_file(self, dst_dir: str, element_name: str):
        with open(path.join(self.get_generated_directory(dst_dir), element_name + ".tsx"), "wt") as fout:
            fout.write(Templates.react_class_component_with_props_and_state(element_name))

    def get_generated_directory(self, dst_dir: str):
        return path.join(dst_dir, self.generated_directory)
