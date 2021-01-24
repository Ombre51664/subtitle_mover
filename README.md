# subtitle_mover
A very basic script that shifts the timecode of a .srt file

## Examples

Changing the offset, typically when the intro is different:

```
python sub_mover.py -i Input_test.srt -o Output_test_plus_1sec.srt -t 00:00:01,000-00:00:02,000;00:00:10,000-00:00:11,000
Output :
scale factor : 1.0
off set : 1000.0ms
```

Changing the scale factor, typically when the framerate is different for instance here the video framerate is read at 29.97 from a 25 fps video (it is probably not a realistic example):

```
python sub_mover.py -i Input_test.srt -o Output_test_to_2997fps.srt -t 00:00:01,000-00:00:01,199
Output :
scale factor : 1.199
off set : 0.0ms
```

Usually what you want to do is find two subtitle time and indicate where you want them afterwards, here is the help :

```
usage: sub_mover.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-t TIMES]

Let's shift some subtitles!!!

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        input file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file
  -t TIMES, --times TIMES
                        The script requires 2 or 4 timestamps to convert file, the format is:
                        T1-T2[;T3-T4], with TX=HHX:MMX:SSX,msX (and msX is 3 digits long)
                        where T1 will become T2 and T3 will become T4

                        so something like this:
                        HH1:MM1:SS1,ms1-HH2:MM2:SS2,ms2[;HH3:MM3:SS3,ms3-HH4:MM4:SS4,ms4]

                        (if only 2 timestamp are passed we are going to assume that T3=T4=00:00:00,000
                        it's when the subs where aligned at the beginning but shift more and more during the movie)
                        Visit https://github.com/Ombre51664/subtitle_mover/blob/main/README.md for an example

                        Math warning: if T1=T3 IT WILL DIVIDE BY 0 !!!
```

## Q&A

### Can I put the same Input file and output file ?

Nope it will erase the input file without a warning!

###  Is your test file just  calling for a copyright infringement suit ?

Oh? Well maybe this script will gain traction then...
