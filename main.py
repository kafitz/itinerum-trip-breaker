# standard modules
import datetime, csv, math, rpy2
# our own classes
from point import Point
from trace import Trace
import config


def init_file(filename, t):
	"""DOCUMENTATION NEEDED"""
	fd = open(filename, "w")
	header = ""
	if t == "activities":
		header = "user_id,sequence,location_id,travel_mode(s),Unknown,start_time\n"
	elif t == "locations":
		header = "user_id,uid,lon,lat,description,time_at\n"
	fd.write(header)
	fd.close()


# Standard format so we can import this module elsewhere.
if __name__ == "__main__":
	user_ids = []
	# get a list of all user_ids in the coordinates file
	with open(config.input_coordinates_file, newline='') as f:
		reader = csv.DictReader(f)
		for row in reader:
			user_ids.append( row['uuid'] )
	# Keep only unique user_id's
	user_ids = list(set(user_ids)) 
	print( len(user_ids),'user(s) to clean' )
	# loop over users calling all the functions for each
	init_file(config.output_activities_file, "activities")
	init_file(config.output_locations_file, "locations")
	u = 1
	for user_id in user_ids:
		# create trace object for this user
		user = Trace(user_id)
		# remove GPS points believed to be in error
		print("User :", u, len(user.points),'points at start for',user_id )
		u += 1
		user.remove_known_error( config.min_accuracy )
		user.remove_sequential_duplicates()
		user.remove_positional_error()
		# this is actually necessary again after positional cleaning
		# ( some angles == 0 )
		user.remove_sequential_duplicates()
		# identify gaps in the data
		user.make_known_subsets()
		# find locations with the cleaned data
		user.get_activity_locations()
		# allocate time
		user.break_trips() 


