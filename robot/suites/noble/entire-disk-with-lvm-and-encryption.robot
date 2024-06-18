*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${CURDIR}/installer.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
# Installer just sometimes randomly exits
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

Entire Disk With LVM Plus Encryption
    Entire Disk With LVM Plus Encryption

Choose Where to Install Ubuntu
    Choose Where to Install Ubuntu

Create Account
    Create Account

Select Timezone
    Select Timezone

Review Installation
    Review Installation

Wait For Install To Finish
    Wait For Install To Finish

Wait For Reboot To Finish
    Wait For Reboot To Finish
