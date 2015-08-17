```
python ptolemy.py -i <csv_file_path>

-i | --in : indicates option to provide device information in the form of a CSV. It's a mandatory argument.
The program currently supports only device information in form of a CSV.

Other optional parameters that can be specified are:-
-u | --user : This parameter can be used for global authentication by specifying a global username which can be used by all hosts. This parameter must always be used  either with -p | --password or -s | --ssh option.
-p | --password : Another parameter can be used for global authentication by specifying a global password which can be used by all hosts for specified global username.
-p | --password : This parameter can be used for global authentication along with global username by specifying a global SSH Private Key File Path which can be used by all hosts.

```