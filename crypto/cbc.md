## Ceebeecee - 80 (Crypto) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-8

### Problem ###
I wrote a CBC implementation! I sure hope I didn't make any mistakes...

### Hint ###
None

## Answer ##

### Overview ###
Reverse the encryption on the flag.enc

### Details ###

Upon opening the ceebeecee binary one will instantly notice a buffer being set to a string "The flag that would be here is censored, you dodo. Why don't you try to decrypt it?". This is the buffer that the program encrypts.

Then the first byte of the string is set to a random time, and it begins encryption.

The general algo is:

```asm
                mov     dword ptr [esp+20h], 0 ; i = 0
                jmp     short loc_80485AE ; enter loop
; ---------------------------------------------------------------------------

loc_8048555:                            ; CODE XREF: main+C7j
                mov     edx, [esp+20h]  ; i
                mov     eax, [esp+24h]  ; str
                lea     ebx, [edx+eax]  ; str+i
                mov     eax, [esp+20h]  ; i
                lea     edx, [eax-1]    ; i-=1
                mov     eax, [esp+24h]  ; str
                add     eax, edx
                movzx   eax, byte ptr [eax] ; str[i-1]
                movzx   edx, al
                mov     ecx, [esp+20h]
                mov     eax, [esp+24h]
                add     eax, ecx
                movzx   eax, byte ptr [eax]
                movzx   eax, al         ; str[i]
                mov     [esp+4], edx
                mov     [esp], eax
                call    crypt           ; xor arg0, arg1
                mov     [ebx], al       ; str[i] ^= str[i-1]
                mov     edx, [esp+20h]
                mov     eax, [esp+24h]
                add     eax, edx
                movzx   eax, byte ptr [eax]
                movsx   eax, al
                mov     [esp], eax      ; c
                call    _putchar        ; putchar(str[i])
                add     dword ptr [esp+20h], 1 ; ++i

loc_80485AE:                            ; CODE XREF: main+5Aj
                mov     ebx, [esp+20h]
                mov     eax, [esp+24h]
                mov     [esp], eax      ; s
                call    _strlen         ; i < strlen(str)
                cmp     ebx, eax
                jb      short loc_8048555 ; i
                mov     eax, 0          ; i >= strlen(str)
                mov     esi, [esp+7Ch]  ; stack sanity check
                xor     esi, large gs:14h
                jz      short loc_80485D9
                call    ___stack_chk_fail
```

So to reverse the effect of this algorithm which is the equivalent of:

```c
// The ptr to the str had 1 added to it before the loop.
for(int i = 1; i < strlen(str + 1); ++i)
{
    str[i] ^= str[i-1];
    putchar(str[i]);
}
```

You simply start from the back and move toward the front.

```c
size_t stSize = 0;
// read_file os a function I made that reads all bytes from a file and returns a pointer to a buffer holding them
// it also spits out the size.
byte* pEnc = read_file("flag_cbc.enc", stSize);
char* szOut = new char[stSize + 1];
memset(szOut, 0, stSize + 1);
for (int i = stSize - 1; i > 0; --i)
{
	pEnc[i] = pEnc[i] ^ pEnc[i - 1];
}
memcpy(szOut, pEnc, stSize);
printf_s("%s\n", pEnc);
```

Which gets the output

```
I were to say so myself, I'd say the flag is something like flag{r3a11y_scr3wed_up_cbc_d1dnt_i}. You'd have to enter it on the site to score the points. I hope you didn't brute force it, though. That'd be lame.
```

### Flag ###

    flag{r3a11y_scr3wed_up_cbc_d1dnt_i}
    
