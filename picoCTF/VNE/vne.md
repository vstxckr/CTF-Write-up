# VNE

![img](/picoCTF/VNE/assets/overview.png)

## OVERVIEW

- This challenge give us a remote server that we need to connect with ssh, and asked us to run the binary file `"bin"` after connected.

![img](/picoCTF/VNE/assets/replace_connected.png)


- After I connected to the server, I check the current home folder of given user and found the bin file.

![img](/picoCTF/VNE/assets/bin_file.png)

![img](/picoCTF/VNE/assets/info_bin.png)

## IDEAS

- The `bin` file requires the `SECRET_DIR` environment variable, I just have no idea with this at the first time.

![img](/picoCTF/VNE/assets/run_bin.png)

- So I check the `/usr/bin/` to know what command that I can use, and I found the `objdump` and `od` command.

![img](/picoCTF/VNE/assets/usr_bin.png)

- I have used the `objdump` but have no idea with bunch of `Assembly` code. So I use `od` to take all binary contents of `bin` and recover it in my computer with `HxD` then put it in IDA to decompile [recovered_bin_file](/picoCTF/VNE/file/bin).

> Note: 
> - After read some write-up from pro, I realize that I can use scp to download that file to my computer instead of above method :grinning:. The reason I don't use scp is that I fail by using it from pico server and can't connect to my local, so stupid :man_facepalming:
> ![img](/picoCTF/VNE/assets/scp_transfer.png)
> - And here is the raw binary [bin](/picoCTF/VNE/file/real_bin). It uses `system()` that is exactly like my later thought :ghost:.
> ![img](/picoCTF/VNE/assets/decompile_p2.png)
> - Thanks for [trhoanglan04's write-up](https://hackmd.io/@trhoanglan04/BkNgwg7xn) cause it is so useful!

- But unfortunately, The pseudo-code in IDA is unreadable :frowning_face:.

![img](/picoCTF/VNE/assets/decompile.png)

- So I check the hint of this challenge (cause it's free! :sunglasses:).

![img](/picoCTF/VNE/assets/hint.png)

- Hm.. `"Check the /root"` and `"Add more instructions to ls"`. I think this will connect with `SECRET_DIR`, so I return to home folder and play with binary file.

- With those clues, I will set the `SECRET_DIR` to `/root` then run the `bin` file and see what will happen.

![img](/picoCTF/VNE/assets/list_root.png)

- Oh :open_mouth:! it lists the contents of `/root` like `ls` command and inside `/root` have a file named `flag.txt`, it looks like high possiblity is flag of this challenge.

- So, what will I do next? Hm... By this time, I still have no idea to leak the content of `flag.txt` file, even if I have nearly everything :confused:.

- I have search all about `file permission on linux`, then `SUID` and `SGID File Permission`, then `privilege escalation` and even `ls command injection?` :skull:. But I don't find useful informations for this challenge.

- But, then I have an idea from this clue: the `bin` file does some thing like `ls` command, so, does it use `execve` syscall? or something like that to execute the shell command? Then I can inject my shell command inside it to read the `flag.txt` file, cause the binary file have root permission for the `/root` folder.

- I did it immediately after that thought flashed. And this is my solution about this challenge.

## RESULT

![img](/picoCTF/VNE/assets/result.png)