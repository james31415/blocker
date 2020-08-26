import twitter

def block_followers(user_id, my_followers, cursor = -1):
	target_user = api.GetUser(
		screen_name = screen_name,
		include_entities = False)
	if target_user.protected:
		print("Can't get followers for {}. User is protected.".format(screen_name))
		return

	print("Trying to block {}'s followers".format(target_user.screen_name))

	while True:
		print("Getting followers. Cursor: {}".format(cursor))
		next_cursor, previous_cursor, followers = api.GetFollowerIDsPaged(
			user_id = user_id,
			cursor = cursor)
		print("Got {} followers".format(len(followers)))

		if next_cursor:
			cursor = next_cursor

		for follower_id in followers:
			block_user(follower_id, my_followers)

		if next_cursor == 0 or next_cursor == previous_cursor:
			break

	print("Blocking followers complete.")

def block_user(user_id, my_followers):
	if user_id in my_followers:
		return

	try:
		blocked_user = api.CreateBlock(
			user_id = user_id,
			include_entities = False,
			skip_status = True)
		print("Blocked {} ({})".format(blocked_user.name, blocked_user.screen_name))
	except twitter.error.TwitterError as e:
		return
	
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
	user_id = api.GetUser(screen_name = screen_name).id

	cursor = -1
	if len(sys.argv) == 3:
		cursor = sys.argv[2]

	print("Getting my followers")
	my_followers = api.GetFollowerIDs()
	block_followers(user_id, my_followers, cursor)

	print("Trying to block {}.".format(screen_name))
	block_user(user_id, my_followers)
	print("Done")
