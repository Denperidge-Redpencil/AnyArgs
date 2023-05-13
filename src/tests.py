from .AnyArgs import AnyArgs
from unittest import TestCase, main

from os import system, getcwd, remove

def test_load_from_file(test_class, file_path, file_content):
    if "/" not in file_path:
        file_path = getcwd() + "/" + file_path

    args = AnyArgs()
    args.add_group("Arguments").add_argument("Argument")
    
    test_class.assertIsNone(args.get_argument("Arguments", "Argument"))
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(file_content)
    
    args.load_args()
    test_class.assertEqual(args.get_argument("Arguments", "Argument"), "Set")
    remove(file_path)


class Tests(TestCase):
    def test_group_existence(self):
        args = AnyArgs()
        self.assertIsNone(args.groups.get("Group That doesn't exist"))

        args.add_group("Group that does exist")
        self.assertIsNotNone(args.groups.get("Group that does exist"))
        
    def test_argument_adding(self):
        assert_text = "You should be able to add & access arguments set in {0} from {1}"

        args = AnyArgs()
        group = args.add_group("Group")

        args.add_argument(
            group_name="Group",
            argument_name="Arg from AnyArgs",  
            cli_flags=["--Arg"],
            default=False)

        group.add_argument( 
            name="Arg from Group",
            cli_flags=["--ArgTwo"],
            default=False
            )

        self.assertIsNotNone(args.groups["Group"].get_argument("Arg from group"),  
                      assert_text.format("Group", "AnyArgs"))
        
        self.assertIsNotNone(group.get_argument("Arg from AnyArgs"),
                      assert_text.format("AnyArgs", "Group"))




    def test_load_arg_from_conf(self):
        test_load_from_file(self, "args.conf", "[Arguments]\nArgument = Set")
    
    def test_load_arg_from_env(self):
        test_load_from_file(self, ".env", "Argument=Set")



if __name__ == "__main__":
    main()