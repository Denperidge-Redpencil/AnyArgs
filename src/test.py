from .AnyArgs.AnyArgs import AnyArgs
from .AnyArgs.argtypes import ARGTYPE_BOOLEAN, ARGTYPE_STRING

args = AnyArgs()
save_conf = args.add_group("Save Configuration")
save_conf.add_argument("To .env", typestring=ARGTYPE_BOOLEAN)
save_conf.add_argument("To conf", typestring=ARGTYPE_BOOLEAN)

args.load_args()


