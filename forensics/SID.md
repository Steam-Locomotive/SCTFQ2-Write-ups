## SID - 60 (Forensics) ##

#### Write-up by GenericNickname

Created: 2015-12-08

### Problem ###

Find the name of the song. Submit your answer as `sctf{Name} (case sensitive)`.

### Files ###
[mystery.sid](http://compete.sctf.io/2015q2/problemfiles/35/mystery.sid)

### Hint ###

Nice tune...

## Answer ##

### Overview ###

Identity what kind of file mystery.sid is and then find the original to get its name.

### Details ###

Opening the file in a hex editor shows that the first 4 bytes of the file are PSID. Some internet research reveals that this is an old file type used for storing music, specifically for Commodore 64 Machines (C64).

The PSID file format normally includes information about the song, but in this case it has been replaced by `[Redacted]`, so we are not going to be able to find the name in the original file.

Some more internet research will lead to this site: [hvsc.c64.org](http://www.hvsc.c64.org). The quickest way to search the database is to download it and grep through it to see if any of the bytes from mystery.sid match with the songs in the database. I found that the best way to get results was to grab some bytes from right under the header, grep seems to have some limitations in doing searches for hex strings. This search can be done with:
```
grep -r --only-matching --byte-offset --binary --text --perl-regexp "\x10\x4c\x09\x10\x4c\x70\x10\x4c\x66"
```

This will return a list of less than 30 songs, and since VLC will play SID files, it is not unreasonable to check this list by hand. Towards the end of the list, the song Berggreen_I_Am by Scarzix will sound the same, and therefore is the solution.

### Flag ###

    sctf{Berggreen I Am}

