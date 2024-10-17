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

Include Proprietary Software
    Include Proprietary Software

Select TPM FDE
    Select TPM FDE

TPM Recovery Key Slide
    TPM Recovery Key Slide

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

Open Terminal
    Open Terminal

Post Install TPM FDE Check
    Post Install TPM FDE Check

Close Terminal
    Close Terminal

Install OpenSSHServer
    Install OpenSSHServer
