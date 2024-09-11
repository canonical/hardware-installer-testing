*** Settings ***
Documentation       Shared resources for installer testing

*** Variables ***
${T}    ${CURDIR}

*** Keywords ***
EzClick
	BuiltIn.Sleep     0.5
	Click LEFT Button
	BuiltIn.Sleep     0.5
	Move Pointer To (100, 100)

Restart Stream
	Restart Video Input
	BuiltIn.Sleep		10

Search
	[Arguments]		${template}		${timeout}=10
	[Documentation]		Kind of like "Optional Match"
	${match}=	Run Keyword And Return Status
	...		VIDEO.Match		${template}		${timeout}
	[return]	${match}

Grub Try Or Install
	[Documentation]		Go through grub screen
	Match	${T}/grub-try-or-install.png	20
	${combo}	Create List		ENTER
	Keys Combo		${combo}

Select Language
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png		180
	Move Pointer To ${T}/next.png
	EzClick

A11y Slide
	[Documentation]		Accessibility Slide
	Match	${T}/a11y.png	20
	Move Pointer To ${T}/next.png
	EzClick

Keyboard Layout
	[Documentation]		Keyboard Layout Slide
	Match	${T}/keyboard-layout.png	20
	Move Pointer To ${T}/next.png
	EzClick

Disable Wired Internet Connection
	[Documentation]		Disable internet connection via the top panel to test an install with no internet
	Move Pointer To (100, 100)
	Move Pointer To ${T}/open-top-panel.png
	EzClick
	Move Pointer To ${T}/click-connection.png
	EzClick
	Move Pointer To ${T}/close-top-panel.png
	EzClick

Internet Connection
	[Documentation]		Connect to the Internet Slide
	Match	${T}/internet-connection.png	20
	Move Pointer To ${T}/next.png
	EzClick

Interactive vs Automated
	[Documentation]		Interactive vs automated installation slide
	Match	${T}/interactive-vs-automated.png		20
	Move Pointer To ${T}/next.png
	EzClick

Default vs Extended
	[Documentation]		Default vs extended installation slide
	Match	${T}/default-vs-extended.png		20
	Move Pointer To ${T}/next.png
	EzClick

Proprietary Software
	[Documentation]		Slide prompting proprietary software installation
	Match	${T}/proprietary-software.png		20
	Move Pointer To ${T}/next.png
	EzClick

Include Proprietary Software
	[Documentation]		Include proprietary software for testing nvidia hardware
	Match	${T}/proprietary-software.png		20
	Move Pointer To ${T}/install-third-party-software.png
	EzClick
	Match	${T}/install-third-party-software-checked.png		20
	Move Pointer To ${T}/next.png
	EzClick

How do you want to install Ubuntu
	[Documentation]		Erase disk etc vs manual
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/next.png
	EzClick

Entire Disk
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/next.png
	EzClick

Entire Disk With ZFS
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack! well, not really.
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	EzClick
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	EzClick
	Move Pointer To ${T}/erase-disk-use-zfs.png
	EzClick
	Move Pointer To ${T}/advanced-features-ok.png
	EzClick
	Match	${T}/check-zfs-selected.png		20
	Move Pointer To ${T}/next.png
	EzClick

Entire Disk With ZFS Plus Encryption
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack!
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	EzClick
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	EzClick
	Move Pointer To ${T}/erase-disk-use-zfs-plus-encryption.png
	EzClick
	Move Pointer To ${T}/advanced-features-ok.png
	EzClick
	Match	${T}/check-zfs-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	EzClick

Disk Passphrase Setup
	[Documentation]		Sets up passphrase for encrypted installations
	Match	${T}/disk-passphrase.png	20
	Move Pointer To ${T}/choose-a-passphrase.png
	EzClick
	${combo}	Create List		TAB
	Type String		ubuntu
	Keys Combo		${combo}
	Keys Combo		${combo}
	BuiltIn.Sleep    3
	Type String		ubuntu
	Move Pointer To ${T}/next.png
	EzClick

Entire Disk With LVM Plus Encryption
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	# temporary hack!
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	EzClick
	# temporary hack over
	Match	${T}/entire-disk.png		20
	Move Pointer To ${T}/advanced-features.png
	EzClick
	Move Pointer To ${T}/erase-disk-use-lvm-plus-encryption.png
	EzClick
	Move Pointer To ${T}/advanced-features-ok.png
	EzClick
	Match	${T}/check-lvm-plus-encryption-selected.png		20
	Move Pointer To ${T}/next.png
	EzClick

Select Erase Disk and Reinstall
	[Documentation]		Erase the entire disk and reinstall
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	EzClick
	Move Pointer To ${T}/next.png
	EzClick

Choose Where to Install Ubuntu
	[Documentation]		Choose the drive to install on - correct one pre-selected
	Match	${T}/choose-where-to-install.png    20
	Move Pointer To ${T}/next.png
	EzClick

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
	EzClick

Select Timezone
	[Documentation]		Select timezone slide
	Match	${T}/select-timezone.png		20
	Move Pointer To ${T}/london.png
	EzClick
	Move Pointer To ${T}/next.png
	EzClick

Review Installation
	[Documentation]		Review installation slide
	Match	${T}/review-installation.png		120
	Move Pointer To ${T}/install-button.png
	EzClick

Wait For Install To Finish
	[Documentation]		Install finished slide
	Match	${T}/install-complete.png		2400
	Move Pointer To ${T}/restart-button.png
	EzClick
	Match	${T}/remove-medium.png		2400
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
	EzClick
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		360

Wait For LVM Encrypted Reboot To Finish
	[Documentation]		Waits for an encrypted reboot to finish, enters passphrase, and logs in
	BuiltIn.Sleep	10
	Restart Video Input
	Match	${T}/lvm-passphrase-input.png		1200
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/login-prompt.png			180
	Move Pointer To ${T}/login-prompt.png
	EzClick
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		360

Wait For ZFS Encrypted Reboot To Finish
	[Documentation]		Waits for an encrypted reboot to finish, enters passphrase, and logs in
	BuiltIn.Sleep	10
	Restart Video Input
	Match	${T}/zfs-passphrase-input.png		1200
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/login-prompt.png			180
	Move Pointer To ${T}/login-prompt.png
	EzClick
	${combo}	Create List		ENTER
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		ENTER
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		360

Skip Installer Update
	[Documentation]		Installer update available slide
	${found}=		Search		${T}/installer-update-available.png		20
	# Need to change this to update but not for now
	IF		${found}
		Move Pointer To ${T}/skip.png
		EzClick
	END

Try Or Install
	[Documentation]		Choose try or install
	Match	${T}/try-or-install.png
	Move Pointer To ${T}/next.png
	EzClick

First Slide Test
	[Documentation]		Select Language, we will default to English
	Match	${T}/language.png	180
	EzClick

Manual Partitioning
	[Documentation]		Manual partitioning, using whole disk
	# THIS DOESN'T WORK ON LAB MACHINES! IT IS A FINNICKY TEST CASE!
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/manual-installation.png
	EzClick
	Move Pointer To ${T}/next.png
	EzClick
	Match	${T}/manual-partitioning-slide.png		20
	Move Pointer To ${T}/free-space.png
	EzClick
	Move Pointer To ${T}/manual-partitioning-plus.png
	EzClick
	Match	${T}/create-partition.png		20
	Move Pointer To ${T}/mount-pount-box.png
	EzClick
	Move Pointer To ${T}/manual-partitioning-select-root.png
	EzClick
	Match	${T}/check-partition.png		20
	Move Pointer To ${T}/next.png
	EzClick

Update Installer
	[Documentation]		Updates the installer snap and reinstalls it
	Match	${T}/installer-update-available.png		20
	Move Pointer To ${T}/update-now.png
	EzClick
	Match	${T}/updating-installer.png		20
	Match	${T}/installer-update-ready.png		300
	Move Pointer To ${T}/close-installer.png
	EzClick

Open Installer
	Move Pointer To ${T}/installer-icon.png
	EzClick

OEM Wait For Reboot To Finish And Do GIS
	[Documentation]		Login Prompt
	#  A sleep here isn't great... but it should do, hopefully...
	BuiltIn.Sleep	10
	Restart Video Input
	Match	${T}/gis-welcome.png		1200
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-typing.png		20
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-network.png		20
	Move Pointer To ${T}/gis-skip.png
	EzClick
	Match	${T}/gis-location-services.png		20
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-timezone.png		20
	Move Pointer To ${T}/gis-timezone-search-cities.png
	EzClick
    Type String     taipei
	Match	${T}/gis-timezone-taipei.png	20
	Move Pointer To ${T}/gis-timezone-taipei-taiwan.png
	EzClick
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-about-you.png		20
    Type String		ubuntu
	Match	${T}/gis-about-you-user-data-filled.png		20
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-set-password.png		20
    Type String		ubuntu
	${combo}	Create List		TAB
	Keys Combo		${combo}
	Keys Combo		${combo}
    Type String		ubuntu
	Move Pointer To ${T}/gis-next.png
	EzClick
	Match	${T}/gis-done.png		20
	Move Pointer To ${T}/gis-start-using-ubuntu.png
	EzClick
	Match	${T}/firefox-icon.png		30

Select TPM FDE
    [Documentation] 	This slide assumes the disk is empty
	Match	${T}/disk-setup.png		20
	Move Pointer To ${T}/erase-disk-install-ubuntu.png
	EzClick
	Move Pointer To ${T}/advanced-features.png
	EzClick
	Match	${T}/tpm-fde-available.png		20
	Move Pointer To ${T}/tpm-fde-available.png
	EzClick
	Match	${T}/tpm-fde-selected.png		20
	Move Pointer To ${T}/advanced-features-ok.png
	EzClick
	Move Pointer To ${T}/next.png
	EzClick

TPM Recovery Key Slide
	[Documentation]		Bluh
	Match	${T}/tpm-recovery-key.png		20
	BuiltIn.Sleep		60
	Move Pointer To ${T}/next.png
	EzClick

Exit Installer
	Match	${T}/exit-installer.png		180
    Move Pointer To ${T}/exit-installer.png
	EzClick
