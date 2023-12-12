# Rhenium

Rhenium 2023  version 0.2.1  (formly Active Installer)

Rhenium is an easy to use automated setup tool to compile and install programs in different software and hardware environments.

---
# Content
* [Why to use Rhenium](#Why-to-use-Rhenium)
* [Get started](#get-started)
* [Automate your software installation](#automate-your-software-installation)
* [Writing your Installation file](#writing-your-installation-file)
    * [Operating System Specific Script](#operating-system-specific-script)
    * [Hardware Specific Script](#hardware-specific-script)
    * [Software Environment specific script](#software-environment-specific-script )
    * [building your installation logic](#building-your-installation-logic)
* [Debug Mode](#debug-mode)
* [Final words](#final-words)

---

# Why to use Rhenium

1. For the end users Rhenium makes installing software or compiling it from
source a lot easier. you just write `rhenium install` then you wait for all the 
magic.

2. For software developers it simplifies the whole automated installation process
in multiple environments for you. You can write shell scripts that are specific
to an operating system, a hardware device, or a piece of software that is 
installed on the targeted system.


# Get started

Rhenium can be installed simply by running this in the command line 
[script](https://raw.githubusercontent.com/Hussein-L-AlMadhachi/Rhenium/main/install.sh)
then it will ask you to select your operating system

NOTE: this may emit some error messages that can be ignored.

``` sh
user@host:~$ sh install.sh
``` 


if you have `installfile` downloaded locally you just navigate to the this file
then you start the setup as shown below

``` sh
user@host:~$ cd  <path to 'InstallFile'>
user@machine:~$ rhenium install
```

if what you want to install is on a remote repository you can download it then
install it directly with this

``` sh
user@host:~$ rhenium clone  <remote repository URL>
```

if you want to change any of the settings

``` sh
user@host:~$ sudo rhenium setup
```

# Automate your software installation

1. You need to have Rhenium installed

2. Create a file called `InstallFile` which we will talk about how to organise
your scripts inside it in the next section.

3. add [`installer.sh`](https://github.com/Hussein-L-AlMadhachi/Rhenium/raw/main/installer.sh)
to the same same location as `InstallFile`.

4. Now the user can install your program by running this `installer.sh`
or use `rhenium install` or clone your remote repository with `rhenium clone ..`


# Writing your Installation file

here is an example of and `Installfile`

``` 
# NOTE: indentation is neglected by Rhenium

pci {NVIDIA}
    echo you have an NVIDIA GPU
end

pci not {NVIDIA}
    echo you do not have an NVIDIA GPU
end


path {/etc/rhenium}
    echo you have Rhenium installed
end



os {debian}
    echo you are using debian
end

os not {debian}
    echo you are not using debian
end


os {fedora} and path {/etc/rhenium} and pci not {NVIDIA} and path not {/etc/apt}
    echo you are using fedora
    echo you are using Rhenium
    echo you do not have an NVIDIA GPU
    echo you are not using apt package manager
end

path {/usr/bin/perl} or path {/usr/bin/python3}
	echo you have either Perl or Python 3 installed 
end

# this is a comment

exec
    # any code here will run anyway
    echo hello world
end

```

## Operating System Specific Script

``` 
os {arch}
    # shell script goes here
    echo you are using Arch linux
end
```

this is for Arch Linux here is a list of all supported operating systems

`{arch}` for Arch Linux  
`{fedora}` for Fedora Linux  
`{opensuse}` for OpenSUSE Linux  
`{cent os}` for CentOS  
`{alpine}` for Apline Linux  
`{gentoo}` for Gentoo Linux  
`{freebsd}` for FreeBSD
`{netbsd}` for NetBSD
`{openbsd}` for OpenBSD  
`{debian}` for Debian Linux  
`{ubuntu}` for Ubuntu Linux  
`{void}` for Void Linux  


if you think we forgot some POSIC complient operating systems create an [issue]([https://github.com/Hussein-L-AlMadhachi/Rhenium/discussions](https://github.com/Hussein-L-AlMadhachi/Rhenium/issues))


## Hardware Specific Script
first use lspci command to list all the devices
```
user@machine:~$ lspci
    ... 
0000:01:00.0 3D controller: NVIDIA Corporation GP107M [GeForce MX350] (rev a1)
    ... 
```

then copy the text are you looking for from the output. here we will take `GeForce MX350` as an example to write a specific shell script for this

``` rudy
pci {GeForce MX350}
    # shell script goes here
    echo you have GeForce MS350 GPU
end
```

## Software Environment specific script

for example operating systems that uses systemd (famous component used in many Linux distros) usually have this path `/run/systemd/system`

``` 
path {/run/systemd/system}
    # shell script goes here
    echo your system uses system
end
```

## building your installation logic

You can use the `not` operator to assign a script if a condition wasn't met

``` 
os not {alpine}
    echo you are not using Alpine Linux
end
```

this also works for `pci` and `path` too.

You can use logical operators `and` and `or` to combine more than one condition and assign a script that is specific to this.

for example:

``` 
os {fedora} and path {/etc/rhenium} and pci {NVIDIA} and path not {/etc/apt}
    echo you are using Fedora Linux
    echo you are using Rhenium
    echo you are using an NVIDIA GPU
    echo you are not using apt package manager
end
```

# Debug Mode

if you ran into any problems there is a debug mode that will detail how it is running your scripts. here is how to run Rhenium in debug mode

instead of regular `rhenium install` you write

``` sh
user@machine:~$ rhenium debug
```

# Final words
Have you seen any problem?  
Do you think there is something we forgot?  
Do you have some ideas about how to improve this program?  

Join our [Community discussions](https://github.com/Hussein-L-AlMadhachi/Rhenium/discussions)  
Report an [Isseue](https://github.com/Hussein-L-AlMadhachi/Rhenium/issues)
