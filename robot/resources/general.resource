*** Settings ***
Documentation       Shared resources related to installer testing


*** Variables ***
${T}    ${CURDIR}


*** Keywords ***
Open Terminal
    ${combo}    Create List    LEFT_ALT    LEFT_CONTROL    t
    Keys Combo    ${combo}
    Match    ${T}/terminal-topbar.png    20

Write OEM Whitelabel
    ${enter}    Create List    ENTER
    Type String    sudo mkdir -p /usr/share/desktop-provision
    Keys Combo    ${enter}
    BuiltIn.Sleep    3
    Type String    sudo bash -c 'echo "mode: oem" > /usr/share/desktop-provision/whitelabel.yaml'
    Keys Combo    ${enter}
    BuiltIn.Sleep    3

Close Terminal
    Match    ${T}/terminal-topbar.png    20
    ${combo}    Create List    LEFT_CONTROL    W
    Keys Combo    ${combo}

Post Install TPM FDE Check
    [Documentation]    Bluh, assumes (& checks) terminal already open
    ${enter}    Create List    ENTER
    Match    ${T}/terminal-topbar.png    20
    Type String    snap list
    Keys Combo    ${enter}
    Match    ${T}/pc-kernel-installed.png    20
    BuiltIn.Sleep    2
    Type String    sudo apt install linux-image-generic
    Keys Combo    ${enter}
    BuiltIn.Sleep    1
    Type String    ubuntu
    Keys Combo    ${enter}
    Match    ${T}/boot-managed-by-snapd.png    20

Install OpenSSHServer
    # this needs to be reworked with snapshots to ensure the package gets installed
    BuiltIn.Sleep    60
    ${enter}    Create List    ENTER
    Open Terminal
    Type String    sudo apt install -y openssh-server
    Keys Combo    ${enter}
    BuiltIn.Sleep    5
    Type String    ubuntu
    Keys Combo    ${enter}
    Match    ${T}/terminal-topbar.png    20
    BuiltIn.Sleep    75
    Close Terminal
