*** Settings ***
Resource    ${KVM_RESOURCES}
#Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Restart Stream
    Restart Stream

First Slide Test
    First Slide Test
