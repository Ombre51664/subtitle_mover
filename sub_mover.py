import os
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="input file")
    parser.add_argument("-o", "--output_file", help="output file")

    parser.add_argument("-t", "--times", help="need 4 timestamps to convert file format: "\
                        "HH1:MM1:SS1,ms1-HH2:MM2:SS2,ms2;HH3:MM3:SS3,ms3-HH4:MM4:SS4,ms4 "\
                        "where T1 will become T2 and T3 will become T4"\
                        "T1 is the time in the subtitle file, and T2 the time where we want it in the video"\
                        "(if only 2 are passed we are going to assume that T3=T4=00:00:00,000"\
                        "Math warning: if T1=T3 I WILL DIVIDE BY 0 !!!")
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
        
 
