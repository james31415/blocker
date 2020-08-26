import twitter

if __name__ == "__main__":
	import sys
	from t import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

	# Create an Api instance.
	api = twitter.Api(consumer_key=CONSUMER_KEY,
					consumer_secret=CONSUMER_SECRET,
					access_token_key=ACCESS_TOKEN,
					access_token_secret=ACCESS_TOKEN_SECRET,
					sleep_on_rate_limit=True)
	
	cursor = -1
	if len(sys.argv) == 2:
		cursor = int(sys.argv[1])

	while True:
		print("Getting blocks. Cursor: {}".format(cursor))
		next_cursor, previous_cursor, my_blocks = api.GetBlocksIDsPaged(cursor = cursor)
		print("Got {} blocks".format(len(my_blocks)))

		if next_cursor:
			cursor = next_cursor

		for user_id in my_blocks:
			user = api.DestroyBlock(user_id = user_id)
			print("Unblocked {} ({})".format(user.name, user.screen_name))

		if next_cursor == 0 or next_cursor == previous_cursor:
			break

	print("Unblocking complete")
