*** Settings ***
Resource    ${KVM_RESOURCES}

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Select Language
	[Documentation]		Select Language, we will default to English - REVERT MOVE POINTER TO AFTER PR MERGED
	Match	${T}/language.png	120
	Move Pointer To ${T}/next.png
	Move Pointer To (520, 414)
	Click LEFT Button

A11y Slide
	[Documentation]		Accessibility Slide
	Match	${T}/a11y.png	10
	Move Pointer To (520, 414)
	Click LEFT Button

Keyboard Layout
	[Documentation]		Keyboard Layout Slide
	Match	${T}/keyboard-layout.png	10
	Move Pointer To (520, 414)
	Click LEFT Button

Internet Connection
	[Documentation]		Connect to the Internet Slide
	Match	${T}/internet-connection.png	10
	Move Pointer To (520, 414)
	Click LEFT Button

Interactive vs Automated
	[Documentation]		Interactive vs automated installation slide
	Match	${T}/interactive-vs-automated.png		10
	Move Pointer To (520, 414)
	Click LEFT Button

Default vs Extended
	[Documentation]		Default vs extended installation slide
	Match	${T}/default-vs-extended.png		10
	Move Pointer To (520, 414)
	Click LEFT Button

Proprietary Software
	[Documentation]		CLICKING NEXT AFTER THIS SLIDE EXITS THE INSTALLER?! Slide prompting proprietary software installation
	Match	${T}/proprietary-software.png		10
	Move Pointer To (520, 414)
	Click LEFT Button

How do you want to install Ubuntu
	[Documentation]		Erase disk etc vs manual
	Match	${T}/how-to-install.png		10
	Move Pointer To (520, 414)
	Click LEFT Button

Select Erase Disk and Reinstall
	[Documentation]		We assume we're wiping a machine here. Not ideal.
	Move Pointer To		${T}/erase-disk-install-ubuntu.jpeg
	Click LEFT Button
	Move Pointer To (520, 414)
	Click LEFT Button

Choose Where to Install Ubuntu
	[Documentation]		Choose the drive to install on - correct one pre-selected
	Match	${T}/choose-where-to-install.jpeg
	Move Pointer To (520, 414)
	Click LEFT Button

Create Account
	[Documentation]		Create the user account - SHOULD WORK AFTER PR!
	Match	${T}/create-your-account.png		10
	${combo}	Create List		TAB
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	Keys Combo		${combo}
	Keys Combo		${combo}
	Type String		ubuntu
	Keys Combo		${combo}
	Move Pointer To (520, 414)
	Click LEFT Button

Select Timezone
	[Documentation]		Select timezone slide
	Match	${T}/select-timezone.png		10
	Move Pointer To (520, 414)
	Click LEFT Button

Review Installation
	[Documentation]		Review installation slide
	Match	${T}/review-installation.png		10
	Move Pointer To ${T}/install-button.png
	Click LEFT Button

Wait For Install To Finish
	[Documentation]		Install finished slide
	Match	${T}/install-complete.png		600
	Move Pointer To ${T}/restart-button.png
	Click LEFT Button
	Match	${T}/remove-medium.png		600
	Unplug USB
	${combo}	Create List		RETURN
	Keys Combo		${combo}

Wait For Reboot To Finish
	[Documentation]		Login Prompt
	Match	${T}/login-prompt.png		600
	${combo}	Create List		RETURN
	Keys Combo		${combo}
	Type String		ubuntu
	Keys Combo		${combo}
	Type String		ubuntu
	${combo}	Create List		RETURN
	Keys Combo		${combo}
	Match	${T}/noble-desktop.png		15
