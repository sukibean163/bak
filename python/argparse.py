import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-dbfile", dest="dbfile", help="db dir", default="lvd.db" )
parser.add_argument("-begin", dest="begin", help="begin", default=90,type=int )
parser.add_argument("-end", dest="end", help="end", default=130,type=int )
parser.add_argument("-time", dest="time", help="time", default=1000,type=int )
args = parser.parse_args()
dbfile=args.dbfile
