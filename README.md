# Ionic Remover

This Python script will help you to get rid of Ionic and Capacitor from your React app. Upon successful deletion, it
will display a summary of how many files have been processed. Most importantly, however, it will show a list of
generated React components or div class names (depending on the conversion settings you choose) so you can easily do
further framework migration.

## Help

```
$ python ionic-remover --help
usage: ionic-remover [-h] [-c {DIV,REACT_COMPONENT}] [-g GENERATED_DIRECTORY] [-i] [-k]
       [-n {KEBAB_CASE,CAMEL_CASE}] [-p PREFIX] [-x EXTENSIONS [EXTENSIONS ...]] SOURCE DESTINATION

Removes Ionic and Capacitor from React project.

positional arguments:
  SOURCE                Ionic project directory
  DESTINATION           destination directory

optional arguments:
  -h, --help            show this help message and exit
  -c {DIV,REACT_COMPONENT}, --convert-to {DIV,REACT_COMPONENT}
                        conversion result type, i.e. what all the Ionic components will become
                        (default: REACT_COMPONENT)
  -g GENERATED_DIRECTORY, --generated-directory GENERATED_DIRECTORY
                        path to generated components which is relative to DESTINATION,
                        e.g. "gen" will create directory DESTINATION/gen (default: gen)
  -i, --copy-included   if set, copies only files with extensions defined by --extensions,
                        if not set, copies all files from Ionic directory (default: False)
  -k, --keep-capacitor  if set, Capacitor imports won't be removed from project (default: False)
  -n {KEBAB_CASE,CAMEL_CASE}, --naming-convention {KEBAB_CASE,CAMEL_CASE}
                        if specified, generated class name will be either kebab-case or CamelCase,
                        if not specified, the naming convention will be dependent on --convert-to argument
                        (default: None)
  -p PREFIX, --prefix PREFIX
                        custom element name prefix, e.g. "my-prefix" will result in
                        className="my-prefix-menu-button" for IonMenuButton
                        (default: kwezal)
  -x EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        all file extensions to process (default: ['.ts', '.tsx', '.js', '.jsx'])

```

## P.S.

No hard feelings, Ionic team.