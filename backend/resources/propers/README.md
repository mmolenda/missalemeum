Pre-generated propers for Masses with complex structure, such like Ash Wednesday or Palm Sunday.
If proper for given day is found here, it will be used, otherwise the program will follow the default path
which is parsing the divinum officium sources.
As Windows does not allow colons in filenames, the colons are replaced with double underscore, so a proper with ID
`sancti:02-02:2:w` will be stored under file `sancti__02-02__2__w.json`.

Pre-generated propers are handled by `utils.get_pregenerated_proper`.