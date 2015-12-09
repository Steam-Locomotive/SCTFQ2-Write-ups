## awe - 65 (Recon) ##

#### Write-up by patil215

Created: 2015-12-08

### Problem ###

Once upon a time, I (Aaron Weiss) lived near a former president of the United States. What was my address at this time?

### Hint ###

Example Format: 1 Infinite Loop, Cupertino, CA 95014

## Answer ##

### Overview ###

Use social media to find awe's family members' names and the cities awe has lived in the past. Cross compare this with a list of living presidents and the cities they lived in. Then lookup awe's family members with the city on White Pages to find the address.

### Details ###

awe, awe, who are you? A quick scan of the "about" page on the sCTF website tells us he's a problem writer.

Searching for his name and comparing the profile picture, we can find him on [Facebook](https://www.facebook.com/aaronweiss74?fref=ts). Googling "Aaron Weiss University of Massachusetts Amherst" (his school on his Facebook page) gives us his [website](http://aaronweiss.us/). From there, we can find his Google Plus [profile](https://plus.google.com/+AaronWeiss74/posts).

Looking at the about page on his Google Plus profile, we see that he currently lives in Massachusetts and has previously lived in New Jersey - New York. Let's compare that to a list of presidents' residences that have been alive during the time awe may have lived there.

Awe is a young adult, so the only presidents that could have been alive at the time are Nixon, Carter, Clinton, H.W. Bush, W. Bush, and Obama. The [Wikipedia article](https://en.wikipedia.org/wiki/List_of_residences_of_Presidents_of_the_United_States#Private_homes_of_the_Presidents) on presidents' current residences shows that the only one that lives in New York is Bill Clinton.

Looking up Bill Clinton's private home says he lives in Chappaqua, New York. It's likely that awe lived here too.

Now for the specific address. We can do an address lookup based on name using [this site](http://www.whitepages.com/). However, awe is a young adult so he most likely does not own any residences in Chappaqua. What we can do is look up a family member's name - perhaps his Mom or Dad.

To find awe's family members, we can go to his [friends](https://www.facebook.com/aaronweiss74/friends) list on Facebook (which is publically viewable) and search for people whose last name is "Weiss". That gives us "Chas", "Emily", "Jennifer", "Pam", "Isis", "Adam", "Brandon", and "Spencer" Weiss. Browsing through the Facebook profiles of each of these people, we can deduce that "Chas" is awe's father.

"Chas" is short for "Charles." Doing a lookup for "Charles Weiss" in "Chappaqua, NY" on WhitePages,  we find a [result](http://www.whitepages.com/name/Charles-Weiss/Chappaqua-NY/be669m8). Unfortunately, this fails to be the flag, so now we look for an alternate site for tracking where people live: [FamilyTreeNow](http://www.familytreenow.com/). 

Repeating the previous search on the new site leads us to [Charles F Weiss](http://www.familytreenow.com/record/Yfw0KbbYSVTFB-6PbhYBgA). There are only three results under Current & Past Adresses that are in Chappaqua, and after trying the one on Maple Avenue, we've solved it!

### Flag ###

	25 Maple Avenue, Chappaqua, NY 10514
