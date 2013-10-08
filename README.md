twitter
=======

General Guidelines
------------------

1. Please provide
    * working code
    * a brief design document explaining what you did
    * a link to a server where your code can be tested.
2. Feel free to search the Web for inspiration, but please do not copy code from anywhere,
   keep it 100% yours.
3. Use Python as your language of implementation. Micro-Frameworks and utility libraries are
   allowed, but not a full blown MVC.


The Test Assignment
-------------------

You are to design and implement the API and server side modules for a simplified twitter-like
social updates site, and a simple AJAX client for it. The application contains users; Each user
can post short text messages, follow other users, and get a feed of the latest updates from the
users he is following. You can also get a global feed for all the users.

1. Implement an HTTP based (ReSTful in the loose sense of the term) API that exposes the
following calls (no need for authentication, choose the format you like):

* CreateUser(UserName)
* PostMessage(UserId, MessageText)
* Follow(FollowingUser, FollowedUser)
* Unfollow(FollwingUser, UnfollowedUser)
* GetFeed(ForUserId) -- the aggregate feed of the users this user is following!
* GetGlobalFeed()

