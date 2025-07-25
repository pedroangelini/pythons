# Cut file excerpt

`ffmpeg -ss 220036.06 -i 'In Times Like These_ Mega Boxed Set [B09Z74TD4Z].m4b' -c copy 'z-In Times Like T
hese Series Outro.m4b'`

- `-ss` seek-start
- `-to` seek-to
- `-t` total time (use instead of -to if needed)

# Concatenate a list of files -- did not work

`ffmpeg -f concat -i mylist.txt -c copy output.wav`

- `-f` makes ffmpeg try to interpret the file format, allowign to parse list of files
does what it says?

# Concatenate using intermediate files

<https://trac.ffmpeg.org/wiki/Concatenate#Usingintermediatefiles>
ffmpeg -i input1.mp4 -c copy intermediate1.ts
ffmpeg -i input2.mp4 -c copy intermediate2.ts
ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy output.mp4

`ffmpeg -i 1-In\ Times\ Like\ These.m4b -c copy intermediate.ts`
`ffmpeg -i z-In\ Times\ Like\ These\ Series\ Outro.m4b -c copy outro.ts`
`ffmpeg -i "concat:intermediate.ts|outro.ts" -c copy 'In Times Like These (Book 1 - In Times Like Theses
Series).m4b'`
