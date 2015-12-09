## Size of a Giant - 110 (Game) ##
#### Writeup by r3ndom_ #####
Created: 2015-12-8

### Problem ###
Grow your character 10x its natural size! That is the power of giants!

### Hint ###
There's a variable somewhere in the code that is set to the character size... Maybe if I could just find it...? Or measure the character, then it could help me find it easier if I have the actual value of it....

[Maybe this link could help](http://securityxploded.com/dll-injection-and-hooking.php). I'm trying to manipulate a variable that should be 30 into 300.
And look! Here's a line of the source I managed to get!
`gl::drawSolidTriangle(Vec2f(300, 300), Vec2f(300 - (s / 2), 300 + s), Vec2f(300 + (s / 2), 300 + s));`

[Another helpful link!](https://libcinder.org/docs/reference/opengl.html)

## Answer ##

### Overview ###
Grow your character bigger or manipulate the check for the size.

Methods:
1) Manipulate the check for your size.
2) Change your size (and don't die to the walls).
3) Decrypt the string.

### Details ###

To manipulate the check for size I began by looking references to the encrypted string, "322505102c192c310521342b011920113f34".

I found this in a function, in a subsection at 0x0040921C.

```asm
loc_40921C:                             ; CODE XREF: sub_409190+37j
                                        ; sub_409190+57j ...
                add     esi, 14h
                cmp     esi, 140h
                jb      short loc_4091C0
                lea     eax, [edi-12Bh]
                cmp     eax, 2
                ja      loc_4092CB
                cmp     byte_568831, 0
                jnz     loc_4092CB
                mov     eax, dword_55C4FC
                sub     esp, 18h
                mov     esi, esp
                mov     dword_55C558, eax
                sub     esp, 18h
                mov     dword_55C55C, ebx
                mov     ecx, esp        ; int
                mov     dword_55C560, 2
                mov     byte_568831, 1
                push    24h             ; size_t
                mov     dword ptr [ecx+14h], 0Fh
                mov     dword ptr [ecx+10h], 0
                push    offset a322505102c192c ; "322505102c192c310521342b011920113f34"
                mov     byte ptr [ecx], 0
                call    sub_40A2D0
                mov     ecx, esi
                call    sub_408C20
                add     esp, 18h
                lea     ecx, [esp+48h+var_1C]
                call    sub_408D30
                add     esp, 18h
                mov     ecx, offset byte_55C610 ; void *
                push    eax             ; void *
                call    sub_409CD0
                cmp     [esp+30h+var_8], 10h
                jb      short loc_4092BF
                push    [esp+30h+var_1C] ; int
                call    j__free
                add     esp, 4
```

Note the conditional at the top that jumps away if a specific condition is not met. The easiest way to do this challenge is simply to change the two conditionals to nops or to jump over them. I chose the latter of these two even though it was probably the harder route its often more enjoyable.

So I wrote a quick dll to get the job done.

```c
// Where to jmp to.
dword g_dwsize = 0x0409243;
__declspec(naked) void __cdecl draw_hk()
{
    // Simple long jmp.
	__asm
	{
		jmp dword ptr ds : [g_dwsize]
	}
}

dword HookThread(LPVOID lpParam)
{
	// This just does a little jmp patch for me, I could use it to jmp directly over but I figured why not
	// make the code flow a bit more obtuse?
	Detour((byte*)0x409230, (byte*)draw_hk, 6);
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
	    // Creating a thread here is the best because it doesn't have a chance to cause deadlock.
		CreateThread(0, 0, COERCE_THREAD(HookThread), 0, 0, 0);
	}
	return TRUE;
}
```

### Flag ###

![](images/game3_flag.PNG)

    sctf{maximumpower}

### Alternative Methods (in brief) ###

Decrypting the string is possible as always. 

There are also many possible modifications that all achieve the same goal of skipping the check, I chose that in particular because it was fairly quick.

Modifying the size variable in the binary would not be a good idea simply because it will kill you instantly on the spawn of your character. Instead the best idea is to do a live change of the size variable after you find it in the binary once you're out of the square.
