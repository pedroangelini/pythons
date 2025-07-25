# strat

## Examples

### primeiro livro

```txt
original:
        |-------|---------|-------|-----|----...---|--------|----|
track   1       2         3       4     5         97       98   99
time    a       b         c       d     e          x        y    z

file 1
o track 1-------2---------3-------4                  97.5--98---99
o time  a       b         c       d                   x.5---y----z
n track 1-------2---------3-------                      4---5----6
n time  a       b         c                            d'   e'   f'

d' = d
e' = y - x.5 + d = y - (x.5 - d)
f' = z - x.5 + d
```

### livro do meio

```txt
original:
        |-------|---------|-------|-----|----...---|--------|----|
track   1       2         3       4     5         97       98   99
time    a       b         c       d     e          x        y    z

file 2
o track 1-------2---2.5           4-----5-...-23     97.5--98---99
o time  a       b   b.5           d-----e-...--m      x.5---y----z
n track 1-------2---              3-----4-...--t'       t'-t'+1-t'+2   
n time  a       b                c'     d'             m'---n'---o'

c' = end of intro = b.5
d' = e - d + b.5
m' = m - d + b.5
n'= m' + y - x.5 = (m - x.5)  + (b.5 - d) + y 
  = y - (x.5 - m) - (d - b.5) = old value - gap 1 - gap 2  
o' = z - (x.5 - m) - (d - b.5)
```

## Conclusion

time value = previous time - sum( gaps before time )

## Strat -

_State machine, parsing all events_

1) get list of all events -- track ends, splits for the book (segment starts/ends)
2) loop through list of events keeping track of state: `in book`, or `in gap` starts In Book because all books start with the intro
    if in book:
    - event is track - increment track counter, add lines like
      TRACK x AUDIO
         TITLE "copy title"
      calculate time based on `time value = previous time - sum( gaps before time )`, add line of INDEX 01 _time_
    - event is end segment - record time for start of gap, switch to `in gap` state
    - else: error out
    if in gap:
    - even is track, ignore
    - event is segment start: increase gap size by difference between current time and last start of gap; record a track start with title, and caculated time
