*** Settings ***
Resource    ${KVM_RESOURCES}
#Resource    ${USB_RESOURCES}
Resource    ${CURDIR}/installer.resource

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Wait For Reboot To Finish
    Wait For Reboot To Finish
