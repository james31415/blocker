# blocker
Command line option to automate blocking twitter users

# Usage
blocker.py SCREEN_NAME [CURSOR]
  SCREEN_NAME - Screen name of user to block
  CURSOR - This number permits restarting the block process if stopped. The cursor is printed periodically when received from the pagination function.

# TODO
* Block users that like a particular tweet

  This will require parsing the HTML of the tweet as the API doesn't have access to the information.

* Have a way to quit and restart blocking

  Blocking takes a long time due to Twitter rate limits. Currently, we can restart blocking for a particular user if we append the cursor to the call.

* Provide a watch functionality

  Because it takes so long to block all the users, I've taken to putting the targets in a text file and iterating over the file in shell. It could be more convenient to have the program handle this.
