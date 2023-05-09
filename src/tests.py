from .AnyArgs.AnyArgs import AnyArgs
from unittest import TestCase, main



class Tests(TestCase):

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



if __name__ == "__main__":
    main()