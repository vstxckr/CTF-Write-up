import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

class code_decom {
    public static void main(String[] args) throws IOException {
        File file = new File("code.jvm");
        FileInputStream fileInputStream = new FileInputStream(file);
        byte[] program = new byte[(int) file.length()];
        fileInputStream.read(program);

        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        int b = 0;
        byte b1 = 0;
        int[] arrayOfInt1 = new int[1024];
        int[] arrayOfInt2 = new int[4];
        while (b < program.length) {
            int i;
            byte b3, b4;
            System.out.printf("%x. ", b);
            switch (program[b]) {
                case 0:
                case 1:
                case 2:
                case 3:
                    b3 = program[b];
                    b4 = program[b + 1];
                    System.out.printf("swapreg %x, %x\n", b3, b4);
                    //i = arrayOfInt2[b3];
                    //arrayOfInt2[b3] = arrayOfInt2[b4];
                    //arrayOfInt2[b4] = i;
                    b += 2;
                    continue;
                case 8:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] += %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] + b4;
                    b += 3;
                    continue;
                case 9:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] += arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] + arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 12:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] -= %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] - b4;
                    b += 3;
                    continue;
                case 13:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] -= arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] - arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 16:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] *= %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] * b4;
                    b += 3;
                    continue;
                case 17:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] *= arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] * arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 20:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] /= %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] / b4;
                    b += 3;
                    continue;
                case 21:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] /= arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] / arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 24:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] %= %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] % b4;
                    b += 3;
                    continue;
                case 25:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] %= arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] % arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 28:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] <<= %x\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] << b4;
                    b += 3;
                    continue;
                case 29:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("arrayOfInt2[%x] <<= arrayOfInt2[%x]\n", b3, b4);
                    //arrayOfInt2[b3] = arrayOfInt2[b3] << arrayOfInt2[b4];
                    b += 3;
                    continue;
                case 31:
                    b3 = program[b + 1];
                    System.out.printf("arrayOfInt2[%x] = read()\n", b3);
                    //arrayOfInt2[b3] = bufferedReader.read();
                    b += 2;
                    continue;
                case 32:
                    System.out.printf("arrayOfInt1[b1] = read()\n");
                    //arrayOfInt1[b1++] = bufferedReader.read();
                    b++;
                    continue;
                case 33:
                    b3 = program[b + 1];
                    System.out.printf("print(arrayOfInt2[b3])\n");
                    //System.out.print((char)arrayOfInt2[b3]);
                    b += 2;
                    continue;
                case 34:
                    System.out.printf("print(arrayOfInt1[b1])\n");
                    //System.out.print((char)arrayOfInt1[--b1]);
                    b++;
                    continue;
                case 41:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("if (arrayOfInt2[%x] == 0): jmp %x\n", b3, b4);
                    //if (arrayOfInt2[b3] == 0) {
                    //  b = b4;
                    //  continue;
                    //} 
                    b += 3;
                    continue;
                case 42:
                    b3 = program[b + 1];
                    b4 = program[b + 2];
                    System.out.printf("if (arrayOfInt2[%x] != 0): jmp %x\n", b3, b4);
                    //if (arrayOfInt2[b3] != 0) {
                    //  b = b4;
                    //  continue;
                    //} 
                    b += 3;
                    continue;
                case 43:
                    b3 = program[b + 1];
                    System.out.printf("jmp %x\n", b3);
                    //b = b3;
                    b += 2;
                    continue;
                case 52:
                    b3 = program[b + 1];
                    System.out.printf("arrayOfInt1[b1++] = arrayOfInt2[%x]\n", b3);
                    //arrayOfInt1[b1++] = arrayOfInt2[b3];
                    b += 2;
                    continue;
                case 53:
                    b3 = program[b + 1];
                    System.out.printf("arrayOfInt2[%x] = arrayOfInt1[--b1]\n", b3, b1);
                    //arrayOfInt2[b3] = arrayOfInt1[--b1];
                    b += 2;
                    continue;
                case 54:
                    b3 = program[b + 1];
                    System.out.printf("arrayOfInt1[b1++] = %x\n", b3);
                    //arrayOfInt1[b1++] = b3;
                    b += 2;
                    continue;
                case 127:
                    System.out.print("return\n");
                    //bufferedReader.close();
                    b++;
                    //return;
            }
            //byte b2 = program[b];
            //b3 = program[b + 1];
            //b4 = program[b + 2];
            //program[b] = (byte)(program[b] ^ b3 ^ b4);
            //program[b + 1] = (byte)(program[b] ^ b2 ^ b4);
            //program[b + 2] = (byte)(program[b + 1] ^ b2 ^ b3);
        }
    }
}
