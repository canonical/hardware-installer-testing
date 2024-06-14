*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${INSTALLER_RESOURCES}

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

Interactive vs Automated
    Interactive vs Automated

Default vs Extended
    Default vs Extended

Proprietary Software
    Proprietary Software

How do you want to install Ubuntu
    How do you want to install Ubuntu

Select Erase Disk and Reinstall
    Select Erase Disk and Reinstall

Choose Where to Install Ubuntu
    Choose Where to Install Ubuntu

Create Account
    Create Account

Select Timezone
    Select Timezone

Review Installation
    Review Installation

Wait For install To Finish
    Wait For install To Finish

Wait For Reboot To Finish
    Wait For Reboot To Finish
