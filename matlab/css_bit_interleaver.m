function [out] = css_bit_interleaver(in)
    intlv_seq = [1:4 53:56 9:12 61:64 17:20 37:40 25:28 45:48 33:36 21:24 41:44 61:64 49:52 5:8 57:60 13:16];
    out = in(intlv_seq);
end