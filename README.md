# SquidReporter
Home of SquidReporter

SquidReporter was born from a need to be efficient as a father during the COVID-19 lockdown.  I had to travel up 2 flights of stairs to check in with my kids and I needed a better solution.  

I was running a firewall at home with the Squid proxy enabled to block common adware, malware, and some categories (e.g. porn) so I started checking the logs to make sure they were spending their time doing the school assigned online work.

If you've ever read Squid Logs or know about how modern websites are built you know that the logs were long and messy.

I checked out SquidAnalyzer (http://squidanalyzer.darold.net/) and found it had the usual content you'd find in most commercial products:

- Top 10 URLs
- View by day
- View by user

This didn't save me time.  I just wanted to know the main URLs that my kids would visit.

Since I was learning Python, I decided to build what I needed as my first project.   (Hint: That is why you will likely not be impressed by my Object Oriented design.)

Hope you enjoy and please give me feedback so we can grow this together.

Requirements:
- MongoDB installed (with a user\password that has permission to read/write from the DB)
- Python 3.7
