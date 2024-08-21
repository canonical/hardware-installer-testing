*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource
Resource    ${CURDIR}/general.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Exit Installer
    Exit Installer

Open Terminal
    Open Terminal

Write OEM WhiteLabel
    Write OEM WhiteLabel

Close Terminal
    Close Terminal

Open Installer
    Open Installer

Language Slide
    Select Language

A11y Slide
    A11y Slide

Keyboard Layout
    Keyboard Layout

Internet Connection
    Internet Connection

Skip Installer Update
    Skip Installer Update

Interactive vs Automated
    Interactive vs Automated

Default vs Extended
    Default vs Extended

Proprietary Software
    Proprietary Software

Select Erase Disk and Reinstall
    Select Erase Disk and Reinstall

Choose Where to Install Ubuntu
    Choose Where to Install Ubuntu

Review Installation
    Review Installation

Wait For Install To Finish
    Wait For Install To Finish

OEM Wait For Reboot To Finish And Do GIS
    OEM Wait For Reboot To Finish And Do GIS

Install OpenSSHServer
    Install OpenSSHServer
