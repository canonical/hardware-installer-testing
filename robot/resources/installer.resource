*** Settings ***
Documentation       Shared resources for installer testing

*** Variables ***
${T}    ${CURDIR}

*** Keywords ***
Search
	[Arguments]		${template}		${timeout}=10
	[Documentation]		Kind of like "Optional Match"
	${match}=	Run Keyword And Return Status
	...		VIDEO.Match		${template}		${timeout}
	RETURN ${match}

Select Language
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png	20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

A11y Slide
	[Documentation]		Accessibility Slide
	Match	${T}/a11y.png	20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Keyboard Layout
	[Documentation]		Keyboard Layout Slide
	Match	${T}/keyboard-layout.png	20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Internet Connection
	[Documentation]		Connect to the Internet Slide
	Match	${T}/internet-connection.png	20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Interactive vs Automated
	[Documentation]		Interactive vs automated installation slide
	Match	${T}/interactive-vs-automated.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Default vs Extended
	[Documentation]		Default vs extended installation slide
	Match	${T}/default-vs-extended.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Proprietary Software
	[Documentation]		CLICKING NEXT AFTER THIS SLIDE EXITS THE INSTALLER?! Slide prompting proprietary software installation
	Match	${T}/proprietary-software.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

How do you want to install Ubuntu
	[Documentation]		Erase disk etc vs manual
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Entire Disk
    [Documentation] This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Entire Disk With ZFS
    [Documentation] This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	Click LEFT Button
	Move Pointer To ${T}/erase-disk-use-zfs.png
	Click LEFT Button
	Move Pointer To ${T}/advanced-features-ok.png
	Click LEFT Button
	Match	${T}/check-zfs-selected.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Entire Disk With ZFS Plus Encryption
    [Documentation] This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	Click LEFT Button
	Move Pointer To ${T}/erase-disk-use-zfs-plus-encryption.png
	Click LEFT Button
	Move Pointer To ${T}/advanced-features-ok.png
	Click LEFT Button
	Match	${T}/check-zfs-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Entire Disk With LVM Plus Encryption
    [Documentation] This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	Click LEFT Button
	Move Pointer To ${T}/erase-disk-use-lvm-plus-encryption.png
	Click LEFT Button
	Move Pointer To ${T}/advanced-features-ok.png
	Click LEFT Button
	Match	${T}/check-lvm-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Select Erase Disk and Reinstall
	[Documentation]		Erase the entire disk and reinstall
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	Click LEFT Button
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Choose Where to Install Ubuntu
	[Documentation]		Choose the drive to install on - correct one pre-selected
	Match	${T}/choose-where-to-install.png    20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Create Account
	[Documentation]		Create the user account - SHOULD WORK AFTER PR!
	Match	${T}/create-your-account.png		20
	${combo}	Create List		TAB
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    2
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Select Timezone
	[Documentation]		Select timezone slide
	Match	${T}/select-timezone.png		20
	Move Pointer To ${T}/london.png
	Click LEFT Button
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

Review Installation
	[Documentation]		Review installation slide
	Match	${T}/review-installation.png		20
	BuiltIn.Sleep    10
	Move Pointer To ${T}/install-button.png
	Click LEFT Button

Wait For Install To Finish
	[Documentation]		Install finished slide
	Match	${T}/install-complete.png		1200
	Move Pointer To ${T}/restart-button.png
	Click LEFT Button
	Match	${T}/remove-medium.png		1200
	Unplug USB
	${combo}	Create List		ENTER
	Keys Combo		${combo}

Wait For Reboot To Finish
	[Documentation]		Login Prompt
	#  A sleep here isn't great... but it should do, hopefully...
	BuiltIn.Sleep	15
	# The command below isn't yet included in the snap.
	Restart Video Input
	Match	${T}/login-prompt.png		600
	Move Pointer To ${T}/login-prompt.png
	Click LEFT Button
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		60

Installer Update Available
	[Documentation]		Installer update available slide
	${found}=		Search		${T}/installer-update-available.png		20
	IF		${found}
		Move Pointer To ${T}/skip.png
		Click LEFT Button
		Move Pointer To (0, 0)
		BuiltIn.Sleep    10
	END

Try Or Install
	[Documentation]		Choose try or install
	Match	${T}/try-or-install.png
	Move Pointer To ${T}/next.png
	Click LEFT Button
	Move Pointer To (0, 0)
	BuiltIn.Sleep    10

First Slide Test
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png	20
