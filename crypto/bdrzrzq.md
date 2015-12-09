## Bdrzrzq - 5 (Cryptography) ##
#### Writeup by GenericNickname

Created: 2015-12-08

### Problem ###

`uapv{wtaad_ldgas-x_pb-paitgpixcv_qtilttc-htepgpidgh_i0-pccdn_etdeat!!!}`

Have fun :)

## Answer ##

### Overview ###

Figure out the cipher and retrieve the flag.

### Details ###

Since this is the first problem of the CTF, it is probably a pretty simple cipher, and the pattern matches one of a Caesar cipher. Sure enough, throwing the cipher text into [this solver](http://www.xarg.org/tools/caesar-cipher/) with a key of `guess` gives the flag.

### Flag ###

    flag{hello_world-i_am-alterating_between-separators_t0-annoy_people!!!}