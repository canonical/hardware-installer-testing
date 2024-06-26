*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Language Slide
    Select Language
