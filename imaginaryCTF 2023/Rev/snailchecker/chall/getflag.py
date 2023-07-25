def get_flag(s):
     t = ''.join([s[i:i+4][::-1] for i in range(0, len(s), 4)])
     print(t)
s = "ftcisoj{uhperp_selbops_m_deeoooboooo}tso"
get_flag(s)
