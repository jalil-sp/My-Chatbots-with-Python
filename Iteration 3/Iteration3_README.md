# Iteration 3

This was the final iteration of the CELL course where I built the EmojiMenuCard.
Here I put together a bot that gives more information on the person chatting as well as
provide the option to order food if they are hungry. This was by far the most fun
iteration. I learned how to build a menu and adaptive cards, and how they are great way
to add user interface and data collection functionality. I believe I’ve gained the skills to
make very useful chatbots.

Within this bot I wanted some of the returned messages to include emojis, for this
I had to use the ‘colon code’ for my emojis. The return emoji would only show up as its
text rendered version and not what we typically think of as an emoji due to emojis not
being supported in RHO. To display user info I made use of the user_info function within
chatbot services to get personalized information based on the user’s company id code.
Some of the information that I made use of includes the user’s position information,
office location, and their business unit.

I learned how to create a menu that contains three different item types: reply,
submenu, and url. To make use of all the item types I created a main menu of the user
information mentioned above and a sub menu of useful links to sites that the user may
frequent in relation to their job.

The last part of this iteration was implementing an adaptive card to create a mini
sub sandwich ordering form that could be validated in multiple ways. An added touch is
that the bot would return back to the user the time of the order, using key value store,
and the office location that the food would be delivered to.
