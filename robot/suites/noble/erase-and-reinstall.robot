*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
#Language Slide
#    Select Language
#
#A11y Slide
#    A11y Slide
#
#Keyboard Layout
#    Keyboard Layout
#
#Internet Connection
#    Internet Connection

# fails before here - update available for installer is finnicky... it may or may not be there... irritating
#Installer Update Available
#    Installer Update Available

# Try Or Install doesn't come up if the installer has exited already and one has clicked Install RELEASE
#Try Or Install
#    Try Or Install
#
#Interactive vs Automated
#    Interactive vs Automated
#
#Default vs Extended
#    Default vs Extended
#
#Proprietary Software
#    Proprietary Software
#
#Select Erase Disk and Reinstall
#    Select Erase Disk and Reinstall
#
#Choose Where to Install Ubuntu
#    Choose Where to Install Ubuntu
#
#Create Account
#    Create Account
#
#Select Timezone
#    Select Timezone
#
#Review Installation
#    Review Installation

Wait For Install To Finish
    Wait For Install To Finish

#Wait For Reboot To Finish
#    Wait For Reboot To Finish
