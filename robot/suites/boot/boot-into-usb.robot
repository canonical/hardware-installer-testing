*** Settings ***
Resource    ${KVM_RESOURCES}
Resource    ${USB_RESOURCES}
Library    Collections

*** Variables ***
${T}    ${CURDIR}

*** Test Cases ***
Enter Boot Menu
    Press Key And Match    F12    ${CURDIR}/boot-menu.png    20

Select And Boot From USB
    ${combo}    Create List    DOWN
    Keys Combo    ${combo}
    Keys Combo    ${combo}
    Keys Combo    ${combo}
    Keys Combo    ${combo}
    Match   ${T}/usb-selected.png       20
    ${combo}    Create List     RETURN
    Keys Combo    ${combo}
    Match   ${T}/grub-menu.png
    Keys Combo    ${combo}
