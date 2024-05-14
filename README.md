Miko is a ssh tool based on Paramiko

It is designed to run any number of unique commands on any number of devices. I developed with solution because most of the ssh scripts I have found require the same configuration to be pushed.

Use:
1.Build a csv input file with the first column containing the IP or hostname of your targets.
2.On the row, for each target add the ssh commands to push to the corrospinding target (from left to right).
3.Commands do not need to match nor the number of commands.

Run:
1.Run the .exe or .py
2.Enter ssh creds (these will be used for all targets)
3.Status of the run is posted in the gui as it runs

Review:
1.An output file similar to the input file will be produced next to the program with the response from each target per command

Troubleshoot:
1.While the scipt is running it writes to a varcsv.csv file
2.Referance this file, if the run is interupted or there is an error.
