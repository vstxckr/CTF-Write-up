import java.lang.*;
 
class josephus {
 
	public int solve(int n) {
		return ~Integer.highestOneBit(n*2) & ((n<<1) | 1);
	}
	public int brute(int n)
	{
		int x = 0;
		josephus t = new josephus();
		for ( char i = 32 ; i <= 126 ; i++ )
		{
			x = (x & 0xffffff00) | (i); 
			for ( char j = 32 ; j <= 126 ; j++ )
			{
				x = (x & 0xffff00ff) | (j << 8); 
				for ( char k = 32 ; k <= 126 ; k++ )
				{
					x = (x & 0xff00ffff) | (k << 8*2); 
					for ( char l = 32 ; l <= 126 ; l++ )
					{
						x = (x & 0x00ffffff) | (l << 8*3); 
						if (t.solve(x)-1 == n)
						{
							System.out.printf("%x ", x);
						}
					}
				}
			}
		}
		return 0;
	}
    public static void main(String[] args)
    {
		josephus t = new josephus();
		int[] a = {0x4ce8c6d2, 0x66ded4f6, 0x6ad0e0ca, 0x64e0bee6, 0x4ad8c4de, 0x60e6beda, 0x3ec8caca, 0x5ededec4, 0x5ededede, 0x7ae8e6de};

		for ( int i = 0 ; i < 10 ; i++ )
		{
			System.out.printf("turn %d: ", i);
			t.brute(a[i]);
			System.out.print("\n");
		}
    }
}
