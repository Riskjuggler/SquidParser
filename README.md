# SquidReporter
Home of SquidReporter

SquidReporter was born from a need to be efficient as a father during the COVID-19 lockdown.  I had to travel up 2 flights of stairs to check in with my kids and I needed a better solution.  

I was running a firewall at home with the Squid proxy enabled to block common adware, malware, and some categories (e.g. porn) so I started checking the logs to make sure they were spending their time doing the school assigned online work.

If you've ever read Squid Logs or know about how modern websites are built you know that the logs were long and messy.

I checked out SquidAnalyzer (http://squidanalyzer.darold.net/) and found it had the usual basic reports you'd find in most commercial InfoSec or network monitoring products:

- Top 10 URLs
- View by day
- View by user

This didn't save me time though.  I just wanted to know the main URLs that my kids would visit and when.

Since I was learning Python, I decided to build what I needed as my first project.   (Hint: That is why you will likely not be impressed by my Object Oriented design.)

------------------------------------------------------------------------------------------------------------

Minimum Software Requirements:

- Squid Proxy
- MongoDB installed (with a user\password that has permission to read/write from the DB)
- Python 3.7+ with PyMongo

You can find information on installing and configuring these requirements at the following:

http://www.squid-cache.org/  
https://www.python.org/downloads/  
https://pypi.org/project/pymongo/

Additional Install Notes:  

You can find Squid as a pre-installed or free add-on package in several Open Source firewall builds.  Here are a few of my favorites.  The advantage of using Squid on these platforms is they come with easy to use instructions that can help you get the most out of Squid by adding on SquidGuard (http://www.squidguard.org/).

https://www.pfsense.org/  
https://opnsense.org/

------------------------------------------------------------------------------------------------------------

Execution Steps

Once you have all these installed, you can run the script by executing the following:

```bash
python3 ./SquidReporter.py
```

Execution notes:

The first time you run this it will ask you for information to save in the config file at:

```bash
<home>/.SquidReporter/squidreporter.conf
```

Note:  I don't yet have this hardened to encrypt your MongoDB password so keep that file safe and consider excluding it from backups unless you are encrypting them!!

------------------------------------------------------------------------------------------------------------

Hope you enjoy and please give me feedback so we can grow this together!!
