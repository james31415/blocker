import twitter

def block_followers(screen_name, my_followers, cursor = -1):
	print("Trying to block {}'s followers".format(screen_name))

	target_user = api.GetUser(
		screen_name = screen_name,
		include_entities = False)
	if target_user.protected:
		print("Can't get followers for {}. User is protected.".format(screen_name))
		return

	while True:
		print("Getting followers. Cursor: {}".format(cursor))
		next_cursor, previous_cursor, followers = api.GetFollowersPaged(
			screen_name = screen_name,
			skip_status = True,
			include_user_entities = False,
			cursor = cursor)
		print("Got {} followers".format(len(followers)))

		if next_cursor:
			cursor = next_cursor

		for follower in followers:
			block_user(follower.screen_name, my_followers)

		if next_cursor == 0 or next_cursor == previous_cursor:
			break

	print("Blocking followers complete.")

def block_user(screen_name, my_followers):
	if screen_name in my_followers:
		print("Didn't block {}: I follow them.".format(screen_name))
		return

	try:
		blocked_user = api.CreateBlock(
			screen_name = screen_name,
			include_entities = False,
			skip_status = True)
		print("Blocked {} ({})".format(blocked_user.name, blocked_user.screen_name))
	except twitter.error.TwitterError as e:
		print("Block failed for user {}. ({})".format(screen_name, e))
	
if __name__ == "__main__":
	import sys
	from t import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

	# Create an Api instance.
	api = twitter.Api(consumer_key=CONSUMER_KEY,
					consumer_secret=CONSUMER_SECRET,
					access_token_key=ACCESS_TOKEN,
					access_token_secret=ACCESS_TOKEN_SECRET,
					sleep_on_rate_limit=True)

	if len(sys.argv) == 1:
		print("Usage:")
		print("{} screen_name [cursor]".format(sys.argv[0]))
		sys.exit()

	screen_name = sys.argv[1]

	cursor = -1
	if len(sys.argv) == 3:
		cursor = sys.argv[2]

	print("Getting my followers")
	my_followers = [user.screen_name for user in api.GetFollowers(
		skip_status = True,
		include_user_entities = False)]
	block_followers(screen_name, my_followers, cursor)

	print("Trying to block {}.".format(screen_name))
	block_user(screen_name, my_followers)
	print("Done")
