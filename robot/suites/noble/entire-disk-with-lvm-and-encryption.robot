*** Settings ***
Resource    ${KVM_RESOURCES}
#Resource    ${USB_RESOURCES}
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

Skip Installer Update
    Skip Installer Update

Try Or Install
    Try Or Install

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

Disk Passphrase Setup
    Disk Passphrase Setup

Create Account
    Create Account

Select Timezone
    Select Timezone

Review Installation
    Review Installation

Wait For Install To Finish
    Wait For Install To Finish

Wait For LVM Encrypted Reboot To Finish
    Wait For LVM Encrypted Reboot To Finish

Install OpenSSHServer
    Install OpenSSHServer
