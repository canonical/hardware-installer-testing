# Current progress
Most testcases are done, tested and all good.

Biggest blocker is no cdimage mirror. Download speed slows down testing.

There have been some false positives in the jenkins jobs. This has since been theoretically minimised with changes to the code, but needs testing again.

TPM FDE test has worked once.
- one of the three machines for TPM FDE has the necessary snippets for enabling tpm fde
- of the other two:
    - One has permanent "No Signal". I've pinged a lab tech on this.
    - The other has very inconsistent KVM/HDMI. It's practically unusable and I'm skeptical of even using this machine in the tests

So we're at a point where we're very nearly production ready. Once we have the cdimage mirror it'll be full speed ahead.

# Todo:
- Test TPM FDE again
- Test gathering of /var/log/installer/* and journalctl -b 0
- Modify the jenkins jobs to make sense
    - Currently, the jenkins jobs are a matrix. The matrix variable is the test case
    - Need to trigger them based on whenever there is new images
    - Need to trigger in a way as to not use one machines resources at the same time
    - this is complicated when we consider we want to test multiple releases
    - AAAA!
