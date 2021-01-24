import os
import argparse,textwrap
from datetime import time,timedelta


def ts2ms(ts_str):
    ts_splits = ts_str.split(":")
    ms_splits = ts_splits[2].split(",")
    return int(ts_splits[0]) * 3600000 + int(ts_splits[1]) * 60000 +  int(ms_splits[0]) * 1000 + int(ms_splits[1])
    
def ms2ts(ms):
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("{:0>2d}:{:0>2d}:{:0>2d},{:0>3d}".format(h,m,s,ms))

def get_sf_af(times):
    sf = (times[1] - times[3]) / (times[0] - times[2])
    af = times[1] - (sf * times[0])
    return sf, af


def get_times(t):
    splits = t.split(";")
    if (len(splits) == 0):
        print ("Wrong times given : (0)")
        quit()
    elif (len(splits) == 1):
        s = splits[0].split("-")
        return [s[0],s[1],"00:00:00,000","00:00:00,000"]
    elif (len(splits) == 2):
        s0 = splits[0].split("-")
        s1 = splits[1].split("-")
        return [s0[0],s0[1],s1[0],s1[1]]
    else:
        print ("Too many times on my hand...")
        quit()

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Let's shift some subtitles!!!", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-i", "--input_file", help="input file")
    parser.add_argument("-o", "--output_file", help="output file")

    parser.add_argument("-t", "--times", help=textwrap.dedent("""\
    The script requires 2 or 4 timestamps to convert file, the format is:
    T1-T2[;T3-T4], with TX=HHX:MMX:SSX,msX (and msX is 3 digits long)
    where T1 will become T2 and T3 will become T4
    
    so something like this:
    HH1:MM1:SS1,ms1-HH2:MM2:SS2,ms2[;HH3:MM3:SS3,ms3-HH4:MM4:SS4,ms4]
    
    (if only 2 timestamp are passed we are going to assume that T3=T4=00:00:00,000 
    it's when the subs where aligned at the beginning but shift more and more during the movie)
    Visit https://github.com/Ombre51664/subtitle_mover/blob/main/README.md for an example

    Math warning: if T1=T3 IT WILL DIVIDE BY 0 !!!"""))
    args =  parser.parse_args()

    times_str=(get_times(args.times))

    times_ms = [ts2ms(t) for t in times_str]
    
    sf, af = get_sf_af(times_ms)
    print("scale factor : " + str(sf))
    print("off set : " + str(af) + "ms")
    with open(args.input_file, "r") as in_file,open(args.output_file, "w")as out_file:
        for l in in_file:
            if ("-->" in l):
                ts = l.split("-->")
                new_t1 = ms2ts(int(ts2ms(ts[0]) * sf + af))
                new_t2 = ms2ts(int(ts2ms(ts[1]) * sf + af))
                out_file.write(new_t1 + " --> " + new_t2 +"\n")
            else:
                out_file.write(l)
        
 
