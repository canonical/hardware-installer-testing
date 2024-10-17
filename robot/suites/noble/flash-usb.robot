*** Settings ***
#Resource    ${USB_RESOURCES}

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Flash Noble USB
    [Documentation]     Flashes the USB with the Noble ISO
    Download and Provision via USB    https://releases.ubuntu.com/noble/ubuntu-24.04-desktop-amd64.iso
