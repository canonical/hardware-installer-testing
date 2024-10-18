*** Comments ***
# after the installer exits, post update, there's no try or install


*** Settings ***
Resource    ${KVM_RESOURCES}
# Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource
Resource    ${CURDIR}/general.resource


*** Variables ***
${T}    ${CURDIR}


*** Test Cases ***
Language Slide
    Select Language

A11y Slide
    A11y Slide

Keyboard Layout
    Keyboard Layout

Internet Connection
    Internet Connection

Update Installer
    Update Installer

Open Installer
    Open Installer

Post Update Language Slide
    Select Language

Post Update A11y Slide
    A11y Slide

Post Update Keyboard Layout
    Keyboard Layout

Post Update Internet Connection
    Internet Connection

Post Update Interactive vs Automated
    Interactive vs Automated

Post Update Default vs Extended
    Default vs Extended

Post Update Proprietary Software
    Proprietary Software

Post Update Select Erase Disk and Reinstall
    Select Erase Disk and Reinstall

Post Update Choose Where to Install Ubuntu
    Choose Where to Install Ubuntu

Post Update Create Account
    Create Account

Post Update Select Timezone
    Select Timezone

Post Update Review Installation
    Review Installation

Post Update Wait For Install To Finish
    Wait For Install To Finish

Post Update Wait For Reboot To Finish
    Wait For Reboot To Finish

Install OpenSSHServer
    Install OpenSSHServer
