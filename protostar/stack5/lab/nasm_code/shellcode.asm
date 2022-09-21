section .text:
	global _start:
_start:
	push 	0xb
	pop 	eax                ; mov 	eax, 0xb
	xor 	edx, edx     	   ; mov 	edx, 0

	push 	edx                ; mov 	eax, "/bin/sh"
	push 	0x68732f2f
	push 	0x6e69622f
	mov 	ebx, esp

	xor 	ecx, ecx           ; mov 	ecx, 0
	int 	0x80
