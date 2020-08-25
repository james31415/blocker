import twitter

def block_followers(screen_name, cursor = -1):
	print("Trying to block {}'s followers".format(screen_name))

	target_user = api.GetUser(screen_name = screen_name)
	if target_user.protected:
		print("Can't get followers for {}. User is protected.".format(screen_name))
		return

	while True:
		print("Getting followers. Cursor: {}".format(cursor))
		next_cursor, previous_cursor, followers = api.GetFollowersPaged(
			screen_name = screen_name,
			cursor = cursor)
		print("Got {} followers".format(len(followers)))

		if next_cursor:
			cursor = next_cursor

		for follower in followers:
			block_user(follower.screen_name)

		if next_cursor == 0 or next_cursor == previous_cursor:
			break

	print("Blocking followers complete.")

def block_user(screen_name):
	try:
		blocked_user = api.CreateBlock(screen_name = screen_name)
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
	block_followers(screen_name, cursor)

	print("Trying to block {}.".format(screen_name))
	block_user(screen_name)
	print("Done")
