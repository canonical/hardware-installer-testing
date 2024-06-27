# Todo:

- Test cases
    - most of these are done
- Step for provisioning the USB with the noble/oracular image
- Shut off machine (from client, we don't want to do that from the actual DUT, that'll be a nightmare) - maybe we can do it via ssh to the DUT? but that sucks butts
- get through bios and boot into installer with robot framework - or whatever

need to reset streaming after reboot? ping client team on this

when merging into main when I'm happy with stuff, squash and make commits all tidy

two things to do to move stuff forward:
- set up something end to end - set up a very simple test, just check the language screen etc and post the html
    - jenkins - need to sort out the connectivity between venonat and the taiwan lab - easier with secrets too - already in internal network
    - github actions - two issues
        - not really meant to periodically trigger a matrix of jobs - have a branch which triggers a matrix of jobs
        - not really the right tool
- set up CI
    - pre-commit to run everything in CI, usual trick
- think about junit output - maybe ping the client team about it
- examples of saving artifacts in qa-jenkins-jobs
- post build actions/archive the artifacts
- check server-jenkins-jobs for examples

I need to also just come up with a list of issues to take to the client team:
- c3 requires auth - can we use api keys instead for automated jobs?
- post reboot image matching just doesn't work, it times out
- need to have the provisioning step to boot into the installer (they're already on this)

Need to reset HID after reboot I believe
Need to set up jenkins secrets which include the zapper ip addresses
