# ResED

## The Plan

ResED is the project which me, Tharidu and David worked on during the 24 hour HackEd Beta - 2018 hackathon hosted
by the computer engineering club.

ResED was meant to be a waveform simulation program which could generate cool waveforms and something you could load
up mp3 files in to watch cool simulations. Sort of like an audio spectrum on steroids!


## The Result

Unfortunately most of the cool things we wanted to do didn't end up getting done. ResED is super rough around the edges
and nearing the last few hours we basically started hacking together the makeshift library we created when we were low
on sleep and motivation.

So the code quality isn't great, but I suppose we managed to make a few cool gifs so its not all bad!
Thanks to the guys over at (EZGIF)[http://ezgif.com] for having such high upload limits so we could make some
cool gifs out of the simulation pictures we made.

Here is a recording of the little in program player of the waveform picture it makes.

![I'm faded](https://github.com/AssortedFantasy/ResED/blob/master/res_ed_nonsense.gif)

A few notes:

* Its supposed to be waves eminating out of a point source ( which you can't see)
* The waves are bouncing off some walls ( which you also can't see )
* Yes the FPS is higher in the player
* Its less faded in the player, but its still not super vibrant.

There is actually quite a lot of functionality in ResED, not very usable for 95% of it, but its still there.
Technically speaking your point sources can be completely arbirtary piecewise functions or whatever.

You can also have arbitrary intital conditions for position and velocity for each particle. Also the
material properties are super flexible in that you can pick the elasticity, damping and density of each individual
pixel. (It basically is done by loading up a .png file which you draw walls and things on)


## The Learning

Learned a lot of things in making this, like collaborative work, how PyGame sorta works, how to do number crunching etc.
Also one of the most important lessons learned is that scientific simulations take a ton of number crunching. Apparently
when scientists make supercomputers for whatever it is they simulate, its not actually to flex on people.

## The Future??? Also how to Run this

Firstly, don't even **bother** trying to run this version of ResED. Its would be more pointful to try and do astrononmy at stone
henge. I think you only need Pygame, numpy, scipy and pillow installed though. The mp3 things need ffmpeg or something. Python 3.6 should work but this was made on 3.7.

There are TONS of things that still need to be added. Like mp3 visualizing, chidini plate patterns, gpu acceleration, etc.
None of which will be done here, just sit tight and wait. Eventually I'll make a ResED Vamped which will do justice to that twinkle
of an idea in my mine.
