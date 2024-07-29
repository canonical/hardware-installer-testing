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
	[return]	${match}

Select Language
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png	20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

A11y Slide
	[Documentation]		Accessibility Slide
	Match	${T}/a11y.png	20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Keyboard Layout
	[Documentation]		Keyboard Layout Slide
	Match	${T}/keyboard-layout.png	20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Disable Wired Internet Connection
	[Documentation]		Disable internet connection via the top panel to test an install with no internet
	Move Pointer To (100, 100)
	Move Pointer To ${T}/open-top-panel.png
	BuiltIn.Sleep	1
	Click LEFT Button
	BuiltIn.Sleep	1
	Move Pointer To ${T}/click-connection.png
	BuiltIn.Sleep	1
	Click LEFT Button
	BuiltIn.Sleep	1
	Move Pointer To ${T}/close-top-panel.png
	BuiltIn.Sleep	1
	Click LEFT Button
	BuiltIn.Sleep	1

Internet Connection
	[Documentation]		Connect to the Internet Slide
	Match	${T}/internet-connection.png	20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Interactive vs Automated
	[Documentation]		Interactive vs automated installation slide
	Match	${T}/interactive-vs-automated.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Default vs Extended
	[Documentation]		Default vs extended installation slide
	Match	${T}/default-vs-extended.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Proprietary Software
	[Documentation]		Slide prompting proprietary software installation
	Match	${T}/proprietary-software.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Include Proprietary Software
	[Documentation]		Include proprietary software for testing nvidia hardware
	Match	${T}/proprietary-software.png		20
	Move Pointer To ${T}/install-third-party-software.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	Match	${T}/install-third-party-software-checked.png		20
	Move Pointer To ${T}/next.png
	Click LEFT Button
	BuiltIn.Sleep     3
	BuiltIn.Sleep    10

How do you want to install Ubuntu
	[Documentation]		Erase disk etc vs manual
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Entire Disk
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Entire Disk With ZFS
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack!
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/erase-disk-use-zfs.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/advanced-features-ok.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/check-zfs-selected.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Entire Disk With ZFS Plus Encryption
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack!
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	Move Pointer To ${T}/erase-disk-use-zfs-plus-encryption.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	Move Pointer To ${T}/advanced-features-ok.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	Match	${T}/check-zfs-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Disk Passphrase Setup
	[Documentation]		Sets up passphrase for encrypted installations
	Match	${T}/disk-passphrase.png	20
	Move Pointer To ${T}/choose-a-passphrase.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	${combo}	Create List		TAB
	Type String		ubuntu
	Keys Combo		${combo}
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Entire Disk With LVM Plus Encryption
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack!
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/erase-disk-use-lvm-plus-encryption.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/advanced-features-ok.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/check-lvm-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Select Erase Disk and Reinstall
	[Documentation]		Erase the entire disk and reinstall
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Choose Where to Install Ubuntu
	[Documentation]		Choose the drive to install on - correct one pre-selected
	Match	${T}/choose-where-to-install.png    20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Create Account
	[Documentation]		Create the user account - SHOULD WORK AFTER PR!
	Match	${T}/create-your-account.png		20
	${combo}	Create List		TAB
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Select Timezone
	[Documentation]		Select timezone slide
	Match	${T}/select-timezone.png		20
	Move Pointer To ${T}/london.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Review Installation
	[Documentation]		Review installation slide
	Match	${T}/review-installation.png		20
	BuiltIn.Sleep    10
	Move Pointer To ${T}/install-button.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3

Wait For Install To Finish
	[Documentation]		Install finished slide
	Match	${T}/install-complete.png		1200
	Move Pointer To ${T}/restart-button.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/remove-medium.png		1200
	Unplug USB
	${combo}	Create List		ENTER
	Keys Combo		${combo}

Wait For Reboot To Finish
	[Documentation]		Login Prompt
	#  A sleep here isn't great... but it should do, hopefully...
	BuiltIn.Sleep	10
	Restart Video Input
	Match	${T}/login-prompt.png		600
	Move Pointer To ${T}/login-prompt.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		60

Wait For LVM Encrypted Reboot To Finish
	[Documentation]		Waits for an encrypted reboot to finish, enters passphrase, and logs in
	BuiltIn.Sleep	10
	# perhaps this is only required for 10.102.234.67?
	Restart Video Input
	Match	${T}/lvm-passphrase-input.png		600
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/login-prompt.png			180
	Move Pointer To ${T}/login-prompt.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		60

Wait For ZFS Encrypted Reboot To Finish
	[Documentation]		Waits for an encrypted reboot to finish, enters passphrase, and logs in
	BuiltIn.Sleep	10
	# perhaps this is only required for 10.102.234.67?
	Restart Video Input
	Match	${T}/zfs-passphrase-input.png		600
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/login-prompt.png			180
	Move Pointer To ${T}/login-prompt.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		60


Skip Installer Update
	[Documentation]		Installer update available slide
	${found}=		Search		${T}/installer-update-available.png		20
	# Need to change this to update but not for now
	IF		${found}
		Move Pointer To ${T}/skip.png
		BuiltIn.Sleep     3
		Click LEFT Button
		BuiltIn.Sleep     3
		Move Pointer To (100, 100)
		BuiltIn.Sleep    10
	END

Try Or Install
	[Documentation]		Choose try or install
	Match	${T}/try-or-install.png
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

First Slide Test
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png	20

Manual Partitioning
	[Documentation]		Manual partitioning, using whole disk
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/manual-installation.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/manual-partitioning-slide.png		20
	Move Pointer To ${T}/free-space.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/manual-partitioning-plus.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/create-partition.png		20
	Move Pointer To ${T}/mount-pount-box.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/manual-partitioning-select-root.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Match	${T}/check-partition.png		20
	Move Pointer To ${T}/next.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	BuiltIn.Sleep    10

Update Installer and Open Installer
	[Documentation]		Updates the installer snap and reinstalls it
	Match	${T}/installer-update-available.png		20
	Move Pointer To ${T}/update-now.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To (100, 100)
	Match	${T}/updating-installer.png		20
	Match	${T}/installer-update-ready.png		300
	Move Pointer To ${T}/close-installer.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
	Move Pointer To ${T}/installer-icon.png
	BuiltIn.Sleep     3
	Click LEFT Button
	BuiltIn.Sleep     3
