# scada_use_case

A quick Splunk app for playing around with the use case described in this Reddit thread: https://www.reddit.com/r/Splunk/comments/kxmotd/how_to_solve_the_following_problem_with_splunk/ (I went with "SCADA" in the name since the dataset seemed like something a SCADA system would spit out).

The app has a little Python event generator, which will output events every 9ish seconds. It outputs to a file rather than to stdout so that you can mess around with the file, if you want. **Be sure to change the output file location in the script itself, if you don't want it to save in the app's log/ directory. Also be sure to change the directories in the app's inputs.conf, if your Splunk is installed elsewhere or you want to save the output file elsewhere.**

The app has a dashboard with a |transaction search on it, which I believe satisfies the use case. The search can probably be done with |stats instead, but for now it works fine and I'm hungry, so I'm going to call it done. The dashboard runs the search looking for events from 2020-01-18, just so results will populate right away, since the sample log included here is from that day; feel free to change the dashboard to whatever timeframe you want, if you're running the even generator. Here's the search itself; I went with "ALFA" and "BRAVO" instead of "event_A" and "event_B" from the Reddit post.
```
index=main sourcetype="scada:log"
| eval EVENT_TEXT_1=substr(EVENT_TEXT, 1, 1),
       EVENT_CHECK=if( match(EVENT_TYPE, "BRAVO"), substr(EVENT_TEXT, 2, 1), null() ),
       EVENT_TARGET_1=if( match(EVENT_TYPE, "ALFA"), tonumber(substr(EVENT_TEXT, 2, 1))-1, null() ),
       EVENT_TARGET_2=if( match(EVENT_TYPE, "ALFA"), substr(EVENT_TEXT, 2, 1), null() ),
       EVENT_TARGET_3=if( match(EVENT_TYPE, "ALFA"), tonumber(substr(EVENT_TEXT, 2, 1))+1, null() ),
       EVENT_TEXT_ALFA=if( match(EVENT_TYPE, "ALFA"), EVENT_TEXT, null() ),
       EVENT_TEXT_BRAVO=if( match(EVENT_TYPE, "BRAVO"), EVENT_TEXT, null() ),
       EVENT_TIME_ALFA=if( match(EVENT_TYPE, "ALFA"), _time, null() ),
       EVENT_TIME_BRAVO=if( match(EVENT_TYPE, "BRAVO"), _time, null() ),
       EVENT_CAT_ALFA=if( match(EVENT_TYPE, "ALFA"), EVENT_CAT, null() ),
       EVENT_CAT_BRAVO=if( match(EVENT_TYPE, "BRAVO"), EVENT_CAT, null() )
| transaction EVENT_TEXT_1 startswith="ALFA" endswith="BRAVO"
| eval EVENT_MATCH_TEXT=if( match(EVENT_CHECK, EVENT_TARGET_1) OR match(EVENT_CHECK, EVENT_TARGET_2) OR match(EVENT_CHECK, EVENT_TARGET_3), "YES", "NO" ),
       EVENT_MATCH_TIME=if( (EVENT_TIME_BRAVO-EVENT_TIME_ALFA)<3601, "YES", "NO" ),
       EVENT_TIME_ALFA=strftime(EVENT_TIME_ALFA, "%Y-%m-%d %H:%M:%S"),
       EVENT_TIME_BRAVO=strftime(EVENT_TIME_BRAVO, "%Y-%m-%d %H:%M:%S")
| where EVENT_MATCH_TEXT="YES" AND ( EVENT_CAT_ALFA="ALARM" OR ( EVENT_CAT_ALFA="CLEARED" AND EVENT_MATCH_TIME="YES" ) )
| table EVENT_TIME_ALFA EVENT_CAT_ALFA EVENT_TEXT_ALFA EVENT_TIME_BRAVO EVENT_CAT_BRAVO EVENT_TEXT_BRAVO
```
