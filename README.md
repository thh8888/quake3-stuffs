# quake3-config
Quake 3 servers config

Instructions for spinning up a Quake 3 Free-For-All Server running on Debian Jessie or newer.

In EC2, launch a t2.micro instance (512MB RAM and 1 vcore should do) using the Quake3-Server Image in AMI images with the zone you want.

Once it's started, login and run:

$ screen -d -m /usr/lib/ioquake3/ioq3ded +exec server.cfg +exec maps.cfg

That's it.  You should be able to connect to it via the Public IP assigned by Amazon.

