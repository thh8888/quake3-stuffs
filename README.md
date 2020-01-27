# Quake 3 Server Stuffs

Setting up a server:
-------------------

Instructions for spinning up a Quake 3 Free-For-All Server running on Debian Jessie or newer.

In EC2, launch a t2.micro instance (512MB RAM and 1 vcore should do) using the Quake3-Server Image in AMI images with the zone you want.

Once it's started, login and run:

$ screen -d -m /usr/lib/ioquake3/ioq3ded +exec server.cfg +exec maps.cfg

That's it.  You should be able to connect to it via the Public IP assigned by Amazon.

**To-Do: Instead of using this AMI image, I will put together a Chef Solo recipe to set up all the required packages (except for pak0.pk3) from the base Debian image.


Getting Logs Statistics:
-----------------------

The file "q3stats.py" is the script that will put data into any MySQL instance (Amazon RDS recommended) that will you a table of stats that include total kills, deaths, suicides, and the count of each weapon used.  Here are the steps you need:

- Spin up you MySQL instance and you will need connectivity to that MySQL instance from where you run this q3stats.py and DB admin rights to the DB.
- Execute "create_table.sql" against that DB instance to create the table
- Run "q3stats.py --file <logfile>" where the log file is the server log file and not the console log file.  The name of this server log file is the name you define in server.cfg.
- You should now be able to see your data getting updated in the table "players" in your DB instance.

Now to visualize the data, you can use Google Spreadsheet to pull the data from your DBS instance.  The sample Google App Script code "getdata.gs" is included here that you can copy and paste into your Google Spreadsheet's Script Editor.  Just need to put in the access endpoint for your DB instance along with DB creditials.


