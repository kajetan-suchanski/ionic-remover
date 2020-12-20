import argparse

from config import *
from ionic_remover import IonicRemover
from naming_convention import NAMING_CONVENTION_NAMES
from result_element import RESULT_ELEMENT_NAMES


def main():
    parser = argparse.ArgumentParser(description="Removes Ionic and Capacitor from React project.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("source", metavar="SOURCE", type=str, help="Ionic project directory")
    parser.add_argument("destination", metavar="DESTINATION", type=str, help="destination directory")
    parser.add_argument("-c", "--convert-to", type=str, default=DEFAULT_CONVERT_TO, choices=RESULT_ELEMENT_NAMES,
                        help="conversion result type, i.e. what all the Ionic components will become")
    parser.add_argument("-g", "--generated-directory", type=str, default=DEFAULT_GENERATED_DIRECTORY,
                        help="""path to generated components which is relative to DESTINATION,
                             e.g. "gen" will create directory DESTINATION/gen""")
    parser.add_argument("-i", "--copy-included", action="store_true",
                        help="if set, copies only files with extensions defined by --extensions, "
                             "if not set, copies all files from Ionic directory")
    parser.add_argument("-k", "--keep-capacitor", action="store_true",
                        help="if set, Capacitor imports won't be removed from project")
    parser.add_argument("-n", "--naming-convention", type=str, default=None, choices=NAMING_CONVENTION_NAMES,
                        help="if specified, generated class name will be either kebab-case or CamelCase, "
                             "if not specified, the naming convention will be dependent on --convert-to argument")
    parser.add_argument("-p", "--prefix", type=str, default=DEFAULT_CUSTOM_ELEMENT_PREFIX,
                        help="""custom element name prefix, e.g. "my-prefix" will result in
                        className="my-prefix-menu-button" for IonMenuButton""")
    parser.add_argument("-x", "--extensions", nargs="+", type=str, default=DEFAULT_FILE_EXTENSIONS,
                        help="all file extensions to process")

    args = parser.parse_args()

    remover = IonicRemover(generated_directory=args.generated_directory,
                           file_extensions=args.extensions,
                           copy_all_files=not args.copy_included,
                           convert_to=ResultElement[args.convert_to],
                           element_prefix=args.prefix,
                           naming_convention=args.naming_convention,
                           remove_capacitor=not args.keep_capacitor)

    remover.remove_ionic_from_react_project(args.source, args.destination)


if __name__ == "__main__":
    main()
