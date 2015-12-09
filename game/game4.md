## Negative Time - 170 (Game) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-8

### Problem ###
In the game engine's FPS limitation algorithm, the current time is logged.

What if the current time were to become negative?

### Hint ###
Game is Windows only. :)

## Answer ##

### Overview ###
Make the time variable go negative.

Methods:
1) Patch the check.
2) Patch the point when variable thats checked it set.
3) Decrypt the string.

### Details ###

This can be found in two ways, going to the next encrypted string or finding uses of the `clock()` function. The variable for fps limitation is set using two `clock()` calls then subtracting the two to determine the frame time. That variable is then referenced to decide whether to print the string.

I went with finding the usage of the encrypted string and found this code.

```asm
loc_4092CB:                             ; CODE XREF: sub_409190+A0j
                                        ; sub_409190+ADj
                cmp     word_568834, 0FF9Ch
                jge     loc_4093E4
                cmp     byte_568833, 0
                jnz     loc_4093E4
                mov     eax, dword_55C4FC
                sub     esp, 18h
                mov     esi, esp
                mov     dword_55C564, eax
                sub     esp, 18h
                mov     dword_55C568, ebx
                mov     ecx, esp        ; int
                mov     dword_55C56C, 2
                mov     byte_568833, 1
                push    24h             ; size_t
                mov     dword ptr [ecx+14h], 0Fh
                mov     dword ptr [ecx+10h], 0
                push    offset a322505102c1a28 ; "322505102c1a282e0d21242110023e192834"
                mov     byte ptr [ecx], 0
                call    sub_40A2D0
                mov     ecx, esi
                call    sub_408C20
                add     esp, 18h
                lea     ecx, [esp+48h+var_1C]
                call    sub_408D30
                mov     esi, eax
                add     esp, 18h
                cmp     esi, offset dword_55C628
                jz      short loc_4093CB
                cmp     dword_55C63C, 10h
                jb      short loc_409365
                push    dword_55C628    ; void *
                call    j__free
                add     esp, 4
```

Note the check at the top against 0xff9c, aka -100. If its less than that the code lets this string print.



```c
// Where to return to.
dword g_dwRet = 0;
// My code to do a little comparison myself and set the flags I want.
__declspec(naked) void mfHook()
{
	__asm
	{
		mov dword ptr ds : [0x568834], -101
		cmp dword ptr ds :[0x568834], 0xff9c
		jmp dword ptr ds : [ g_dwRet ]
	}
}

dword HookThread(LPVOID lpParam)
{
	g_dwRet = Detour((byte*)0x4092CB, (byte*)mfHook, 8);
	return 0;
}

#define COERCE_THREAD(a) reinterpret_cast<LPTHREAD_START_ROUTINE>(a)

BOOL WINAPI DllMain(
	_In_ HINSTANCE hinstDLL,
	_In_ DWORD     fdwReason,
	_In_ LPVOID    lpvReserved
	)
{
	if (fdwReason == DLL_PROCESS_ATTACH)
	{
		HookThread(0);
		//CreateThread(0, 0, COERCE_THREAD(HookThread), 0, 0, 0);
	}
	return TRUE;
}
```

This is kind of a long way to do it, but its the first that came to mind. Again patching the compare with nops would have taken less time but I think it also has less finesse. Some games do hash checks on themselves and as such modifying the binary itself can be dangerous.

### Flag ###

![](images/game4_flag.PNG)

    sctf{negamegatime}

### Alternative Methods (in brief) ###

Decrypting the string is possible as always. 

There are also many possible modifications that all achieve the same goal of skipping the check, I chose that in particular because it was fairly quick.

The other code for setting the word that gets checked is at 0x408E33 in the binary. Its something like:

```c
word begin = clock();
// Do something that I guess is drawing, it doesn't do any calls in here so I don't know what exactly to make of it
// without reversing more... Its just like a loop where it sets variables in a struct array.
word_568834 = begin - clock();
```

Which of course is trivial to modify. Also it should probably be clock() - begin to avoid people with trash frames from getting the flag... But to each his own code, I guess.
